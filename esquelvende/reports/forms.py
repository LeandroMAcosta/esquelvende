from django import forms
from .models import Report
from django.utils.translation import ugettext_lazy as _


class FormReport(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['reason',
                  'description',
                  ]

        labels = {
            'reason': _("Por que quieres denunciar esta publicacion?"),
            'description': _("Danos mas detalle de tu denuncia:")
        }
