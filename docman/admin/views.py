from flask import render_template, abort, flash, url_for, redirect
from flask_login import login_required, current_user
from . import admin
from ..auth.forms import EditProfileForm
from .. import db
from ..document.views import my_documents
from .forms import RoleForm
from ..models import Role, User


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/roles')
@login_required
def get_roles():
    """
    List all available roles
    """
    check_admin()
    roles = Role.query.all()

    return render_template('admin/roles/roles.html', roles=roles, title="Roles")


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Adds a role to the list of roles
    :param id: id of the role to be deleted
    :return: the roles page
    """
    check_admin()
    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(title=form.title.data)

        try:
            db.session.add(role)
            db.session.commit()
            flash('New role successfully created')
        except:
            flash('Error: Role title already exist')

        return redirect(url_for('admin.get_roles'))

    return render_template('admin/roles/role.html', form=form, add_role=add_role, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.title = form.title.data

        try:
            db.session.add(role)
            db.session.commit()
            flash('Role successfully edited')
        except:
            flash('Error: Role title already exist')

        return redirect(url_for('admin.get_roles'))

    form.title.data = role.title
    return render_template('admin/roles/role.html', form=form, title='Edit Role', add_role=add_role)


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role
    :param id: id of the role to be deleted
    :return: the roles page
    """
    check_admin()
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have deleted a role')

    return redirect(url_for('admin.get_roles'))


@admin.route('/users')
@login_required
def get_users():
    """
    List all registered users
    """
    check_admin()
    users = User.query.all()

    return render_template('admin/users/users.html', users=users, title="All Users")


@admin.route('/user/<int:id>')
@login_required
def get_user(id):
    """
    Open the profile page of a user
    """
    if current_user.id == id or current_user.is_admin:
        user = User.query.get_or_404(id)
        documents = my_documents(user.id)
        return render_template('admin/users/user.html', user=user, documents=documents, title="My Profile")
    else:
        abort(403)


@admin.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """
    Lets a user edit their profile
    """
    new_account = False
    profile_to_edit = User.query.get_or_404(id)
    form = EditProfileForm(obj=profile_to_edit)
    if form.validate_on_submit():
        profile_to_edit.name = form.name.data
        profile_to_edit.username = form.username.data
        profile_to_edit.email = form.email.data
        try:
            db.session.add(profile_to_edit)
            db.session.commit()
            flash('You have successfully edited your profile')
        except:
            flash('Aww... Something went wrong, please try again')

        return redirect(url_for('admin.get_user', id=profile_to_edit.id))

    form.name.data = profile_to_edit.name
    form.username.data = profile_to_edit.username
    form.email.data = profile_to_edit.email

    return render_template('auth/register.html', form=form, title="Edit Profile", new_account=new_account)
