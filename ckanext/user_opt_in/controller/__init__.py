import ckan.plugins.toolkit as toolkit
import simplejson
from ckanext.user_ext.controller import UserExt
from ..model import UserOptInModel


class UserOptInController(UserExt):

    def is_opted_in(self, user_id):
        if user_id is None:
            raise RuntimeError("User id must be provided.")
        opted = UserOptInModel.get_opt_in(user_id)
        return opted is True

    def is_opted_out(self, user_id):
        if user_id is None:
            raise RuntimeError("User id must be provided.")
        opted = UserOptInModel.get_opt_in(user_id)
        return opted is False

    def is_opted_in_unknown(self, user_id):
        if user_id is None:
            raise RuntimeError("User id must be provided.")
        opted = UserOptInModel.get_opt_in(user_id)
        return opted is None

    def set_opted_in(self, user_id, state):
        if user_id is None:
            raise RuntimeError("User id must be provided.")
        UserOptInModel.set_opt_in(user_id, state)

    def set(self, *args, **kwargs):
        try:
            request = toolkit.request
            response = toolkit.response
            abort = toolkit.abort
        except Exception, e:
            raise RuntimeError(e)

        params = request.params
        if str(request.method).upper() == "POST":
            if str(request.content_type).lower() == "application/json":
                params = simplejson.loads(request.body)

        if 'opted_in' in params:
            is_opted_in = bool(params['opted_in'])
            try:
                this_user = toolkit.c.userobj.id
            except Exception, e:
                abort(500, 'User is not logged in.')
            self.set_opted_in(this_user, is_opted_in)
            response.content_type = "application/json"
            return simplejson.dumps({"status": "OK"})
        abort(403, 'Must pass in opted_in as bool')

