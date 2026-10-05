import asyncio
import argparse

from app.database import get_db_session
from app.auth_utils import AuthHelper
from app.models import User, UserRole
from app.crud import UserCrudManager


async def create_admin(name: str, username: str, email: str, password: str):
    session_factory = get_db_session()
    session = await anext(session_factory)

    user = await UserCrudManager.select_by_username_or_email(session, username, email)
    if user:
        raise ValueError("User exsits")

    admin = User(
        name=name,
        username=username,
        email=email,
        hashed_password=AuthHelper.password_util.hash(password),
        user_role=UserRole.ADMIN,
    )
    await UserCrudManager.add(session, admin)

    await session.close()
    await session_factory.aclose()

    print("Admin created")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # name
    parser.add_argument("-n", "--name", type=str, required=True, help="Admin's name")

    # username
    parser.add_argument(
        "-u", "--username", type=str, required=True, help="Admin's username"
    )

    # email
    parser.add_argument("-e", "--email", type=str, required=True, help="Admin's email")

    # password
    parser.add_argument(
        "-p", "--password", type=str, required=True, help="Admin's password"
    )

    args = parser.parse_args()

    asyncio.run(create_admin(args.name, args.username, args.email, args.password))
