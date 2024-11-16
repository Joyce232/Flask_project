from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)],
                           render_kw={'Placeholder': 'Nome de usuário'})
    email = StringField(validators=[DataRequired(), Length(min=5, max=50)],
                        render_kw={'placeholder': 'Meu@email.com'})
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={'placeholder': '****'})
    password_confirm = PasswordField('Confirmar Senha', validators=[DataRequired(), Length(min=2, max=20)],
                             render_kw={'placeholder': '****'})
    submit = SubmitField('Entrar')


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Length(min=5, max=50)],
                        render_kw={'placeholder': 'Meu@email.com'})
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={'placeholder': '****'})
    submit = SubmitField('Entrar')


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=2, max=80)],
                        render_kw={'placeholder': 'Título'})
    description = StringField('Descrição', validators=[DataRequired()],
                              render_kw={'placeholder': 'Descreva o assunto do seu post'})
    content = CKEditorField('Conteúdo', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class CommentForm(FlaskForm):
    message = TextAreaField('Mensagem', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SearchForm(FlaskForm):
    searched = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Sua pesquisa aqui'})
    submit = SubmitField('Pesquisar')