# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.exceptions import TemplateDoesNotExist


class BaseMailApi:

    @classmethod
    def _format_mail(cls, lang, template_name, to_email, **ctx):
        """
        Formats and returns the subject and message body using the supplied template name and  context
        :param template_name:
        :param to_email:
        :param ctx:
        :return:
        """
        # Augment the context with common context
        ctx.update(dict(
            site=settings.SITE_URL,
            email=to_email
        ))

        # Render the subject
        subject_template_name = '{template_name}/{template_name}_subject_{lang}.txt'.format(template_name=template_name, lang=lang)
        subject = render_to_string(subject_template_name, context=ctx)

        # Force subject to a single line to avoid header-injection issues.
        subject = ''.join(subject.splitlines())

        # Render the message body (plain/text)
        message_template_name = '{template_name}/{template_name}_{lang}.txt'.format(template_name=template_name, lang=lang)
        message = render_to_string(message_template_name, context=ctx)

        # Render the message body (html) if one exists
        message_template_name = '{template_name}/{template_name}_{lang}.html'.format(template_name=template_name, lang=lang)

        try:
            html_message = render_to_string(message_template_name, context=ctx)
        except TemplateDoesNotExist:
            html_message = None

        return subject, message, html_message

    @classmethod
    def _send_mail(cls, lang, to_email, template_name, from_email=None, **ctx):
        """
        Sends the email to specified address using the specified template and provided context
        :param basestring to_email: the recipient address
        :param basestring template_name: the name of a template
        :param from_email: from email to use
        :param ctx: the context to render with
        :return:
        """
        subject, message, html_message = cls._format_mail(lang=lang, template_name=template_name, to_email=to_email, **ctx)
        # Actually send the email
        return send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email]
        )
