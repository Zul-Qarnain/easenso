CREATE VIEW group_perms_view AS
SELECT auth_group_permissions.*, auth_permission.codename, auth_permission.name,
       django_content_type.model
FROM auth_group_permissions INNER JOIN auth_permission ON
auth_permission.id = auth_group_permissions.permission_id
INNER JOIN django_content_type ON
django_content_type.id = auth_permission.content_type_id;
