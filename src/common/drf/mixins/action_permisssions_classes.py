class ActionPermissionClassesMixin(object):
    def get_permissions(self):
        if self.action_permission_classes and self.action in self.action_permission_classes:
            permissions = self.action_permission_classes[self.action]
            return [permission() for permission in permissions]

        return super(ActionPermissionClassesMixin, self).get_permissions()
