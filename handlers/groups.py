import logging
import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from handlers import BaseHandler, user_authenticate

from google.appengine.ext import ndb
from models.user import User
from models.group import Group
from models.message import Message

app = micro_webapp2.WSGIApplication()

@app.api('/groups')
class GroupsHandler(BaseHandler):

    @user_authenticate
    def post(self):
        if not self.json_body.get('name'):
            return self.res_error('name is required')
        self.json_body['owner'] = self.user.key
        self.json_body['members'] = [self.user.key]
        group = Group.create(self.json_body)
        return self.res_json(group.to_dict())

    @user_authenticate
    def get(self):
        groups = Group.query().order(-Group.create_time).fetch()
        return self.res_json({'result': [group.to_dict() for group in groups]})

@app.api('/groups/<group_id>')
class GroupHandler(BaseHandler):

    @user_authenticate
    def get(self, group_id):
        group = Group.get_by_id(long(group_id))
        if group:
            return self.res_json(group.to_dict())
        else:
            self.abort(404)

    @user_authenticate
    def put(self, group_id):
        group = Group.get_by_id(long(group_id))
        if group:
            if not group.owner == self.user.key:
                self.abort(403)
            user_ids = self.json_body.get('members')
            if user_ids:
                users = [ndb.Key(User, long(user_id)) for user_id in user_ids]
                group.members = users
                group.put()
            return self.res_json(group.to_dict())
        else:
            self.abort(404)

@app.api('/groups/<group_id>/join')
class GroupJoinHandler(BaseHandler):

    @user_authenticate
    def post(self, group_id):
        group = Group.get_by_id(long(group_id))
        if not group:
            self.abort(404)

        group.pending_members.append(self.user.key)
        group.put()
        return self.res_json(group.to_dict())

@app.api('/groups/<group_id>/msg')
class GroupMsgHandler(BaseHandler):

    @user_authenticate
    def get(self, group_id):
        msgs = Message.query(Message.group==ndb.Key(Group, long(group_id))).order(-Message.create_time).fetch()
        return self.res_json({'result': [msg.to_dict() for msg in msgs]})


    @user_authenticate
    def post(self, group_id):
        group = Group.get_by_id(long(group_id))
        if not group:
            self.abort(404)
        # activated
        if self.user.key in group.members:
            sender = self.user.key
            msg_type = self.json_body.get('msg_type')
            content = self.json_body.get('content')

            msg = Message(sender=sender, msg_type=msg_type, content=content, group=group.key)
            msg.put()
        return self.res_json(msg.to_dict())
