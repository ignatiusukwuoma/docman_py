from flask import flash, url_for, redirect, render_template
from flask_login import login_required, current_user
from . import document
from .forms import CreateDocument
from sqlalchemy import desc, and_, or_, not_, select

from .. import db
from ..models import Document, User, Role


@document.route('/document/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    Handles requests to the /create route
    :return: login or register page
    """
    add_document = True
    form = CreateDocument()
    if form.validate_on_submit():
        print('Current User ID', current_user.id)
        new_document = Document(
            title=form.title.data,
            access=form.access.data,
            content=form.content.data,
            user_id=current_user.id,
        )

        # add document to database
        db.session.add(new_document)
        db.session.commit()

        flash('You have created a new document.')

        return redirect(url_for('document.get_documents'))

    return render_template('document/create.html', title='Create Document', form=form, add_document=add_document)


@document.route('/documents')
@login_required
def get_documents():
    """
    Get all documents the user is permitted to view
    :return: documents page
    """
    same_role = User.query.filter_by(role_id=current_user.role_id).all()
    same_role_list = [user.id for user in same_role]

    documents = db.session.query(Document).join("user", "role"). \
        filter(or_(Document.access == 'public',
                   Document.user_id == current_user.id,
                   (and_(Document.access == 'role', Document.user_id.in_(same_role_list))))). \
        order_by(desc(Document.created_at)).all()

    return render_template('document/documents.html', documents=documents, title='All Documents')


def my_documents(id):
    """
    :return: the documents of the user
    """
    documents = db.session.query(Document). \
        filter(Document.user_id == id). \
        order_by(desc(Document.created_at)).all()
    return documents


@document.route('/documents/me')
@login_required
def get_my_documents():
    """
    Get all documents owned by the user
    :return: my documents page
    """
    documents = my_documents(current_user.id)

    return render_template('document/documents.html', documents=documents, title='My Documents')


@document.route('/document/<int:id>', methods=['GET'])
@login_required
def get_document(id):
    """
    Opens up a document
    :param id: the document id
    :return: the single document page
    """
    doc = Document.query.get_or_404(id)

    return render_template('document/document.html', document=doc, title="Single Document")


@document.route('/document/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_document(id):
    """
    Edit a document
    :param id: document id to be edited
    :return: the documents page
    """
    add_document = False
    document_to_edit = Document.query.get_or_404(id)
    form = CreateDocument(obj=document_to_edit)
    if form.validate_on_submit():
        document_to_edit.title = form.title.data
        document_to_edit.access = form.access.data
        document_to_edit.content = form.content.data
        try:
            db.session.add(document_to_edit)
            db.session.commit()
            flash('You have successfully edited a document')
        except:
            flash('Error: Document title already exists')

        return redirect(url_for('document.get_document', id=document_to_edit.id))

    form.title.data = document_to_edit.title
    form.access.data = document_to_edit.access
    form.content.data = document_to_edit.content
    return render_template('document/create.html', form=form, title="Edit Document", add_document=add_document)


@document.route('/document/delete/<int:id>', methods=['GET'])
@login_required
def delete_document(id):
    """
    Delete a document
    :param id: id of the document
    """
    doc = Document.query.get_or_404(id)
    if doc.user_id == current_user.id:
        db.session.delete(doc)
        db.session.commit()
        flash('You have deleted a document')

        return redirect(url_for('document.get_documents'))

    flash('You do not have permission to delete this document')
    return redirect(url_for('document.get_documents'))



