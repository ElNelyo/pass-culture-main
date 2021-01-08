from pcapi.core.users.models import User
from pcapi.repository.user_queries import keep_only_webapp_users
from pcapi.sandboxes.scripts.utils.helpers import get_beneficiary_helper


def get_webapp_user_with_not_validated_password():
    query = keep_only_webapp_users(User.query)
    query = query.filter(User.resetPasswordToken != None)
    user = query.first()

    return {"user": get_beneficiary_helper(user)}
