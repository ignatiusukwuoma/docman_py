from flask import render_template, abort, flash, url_for, redirect
from flask_login import login_required, current_user
from . import admin
from .. import db

from .forms import RoleForm
from ..models import Role


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

    return render_template(title='Delete Role')