from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.settings.config import settings
import pyotp
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import yagmail
from app.settings.oauth import get_current_user, verify_access_token, create_access_token, authenticate_user
from datetime import timedelta
from app.settings import utils, oauth
from app.models.user import User
from app.schemas.user_schema import UserSignInRequest, UserVerification, UserOut
from app.schemas.token_schema import TokenData, Email
from app.settings.database import get_db

app_passwd = settings.app_passwd
app_email = settings.app_email

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


def send_reset_mail(email, token):
    msg = f'''
        To reset your password visit the following link:{token} 
        If you did not make this request then simply ignore this email) 
    '''

    with yagmail.SMTP(app_email, app_passwd) as yag:
        yag.send(to=email, subject='Password Reset Request', contents=msg)


def send_signup_mail(email, token):
    msg = f''' 
           To Sign up on DevAsk, use this code to verify your email :
            {token}   

            If you did not make this request, Simply ignore this email '''

    with yagmail.SMTP(app_email, app_passwd) as yag:
        yag.send(to=email, subject='DevAsk Email Verification', contents=msg)


@router.post('/signin')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_verified:
        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires)

        return {
            "data": {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "name": user.first_name + user.last_name
            },
            "access_token": access_token,
            "token_type": "bearer"}
    return HTTPException(status_code=401, detail="Verify your email to login")


totp = ''


@router.post('/send_email_code', status_code=status.HTTP_200_OK)
def user_signnup(request: Email):
    global totp
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key, interval=600)
    send_signup_mail(request.email, totp.now())
    return {"msg": "email sent"}


def auth_otp(code):
    return totp.verify(code)


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def user_signnup(user_credentials: UserSignInRequest, db: Session = Depends(get_db)):
    user_credentials.password = utils.hash(user_credentials.password)
    user = db.query(User).filter(
        User.email == user_credentials.email).first()

    if user:
        return HTTPException(status_code=400, detail={"msg": "User already exists"})

    new_user = User(username=user_credentials.username,
                    first_name=user_credentials.firstname,
                    last_name=user_credentials.lastname,
                    email=user_credentials.email,
                    password=user_credentials.password,

                    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user = db.query(User).filter(
        User.email == user_credentials.email).first()
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {
        'Success': True,
        'Message': 'user added successfully',
        'data':
            {
                'user_id': user.user_id,
                'userName': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
            },
        'Token': access_token,
        'Token_type': 'Bearer'}


@router.post('/verify-email', status_code=status.HTTP_202_ACCEPTED)
def verify_email(credentials: UserVerification, db: Session = Depends(get_db)):
    if auth_otp(code=credentials.verification_code):
        user = db.query(User).filter(
            User.email == credentials.email)
        if user:
            user.update({'is_verified': True})
            db.commit()
            return {"success": True, "msg": "Email verified"}
        else:
            return HTTPException(status_code=404, detail="User with the current email doesn't exists")
    else:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                            detail="OTP is either a wrong one or has expired ")
