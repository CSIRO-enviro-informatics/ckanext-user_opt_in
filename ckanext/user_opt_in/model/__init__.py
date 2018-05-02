from ckanext.user_ext.model import UserExt

class UserOptInModel(UserExt):
    @classmethod
    def get_opt_in(cls, user_id):
        if user_id is None:
            raise RuntimeError("User id must be provided.")
        res = cls.get_cols(user_id, 'opted_in')
        if res is None:
            return None
        return res.opted_in

    @classmethod
    def set_opt_in(cls, user_id, state):
        if user_id is None:
            raise RuntimeError("User id must be provided.")
        res = cls.set_cols(user_id, opted_in=state)
        return res

