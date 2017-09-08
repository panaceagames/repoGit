# -*- coding: utf-8 -*-
from django import forms
import datetime

_dias = (
        (u'1', u'1'),
        (u'2', u'2'),
        (u'3', u'3'),
        (u'4', u'4'),
        (u'5', u'5'),
        (u'6', u'6'),
        (u'7', u'7'),
        (u'8', u'8'),
        (u'9', u'9'),
        (u'10', u'10'),
        (u'11', u'11'),
        (u'12', u'12'),
        (u'13', u'13'),
        (u'14', u'14'),
        (u'15', u'15'),
        (u'16', u'16'),
        (u'17', u'17'),
        (u'18', u'18'),
        (u'19', u'19'),
        (u'20', u'20'),
        (u'21', u'21'),
        (u'22', u'22'),
        (u'23', u'23'),
        (u'24', u'24'),
        (u'25', u'25'),
        (u'26', u'26'),
        (u'27', u'27'),
        (u'28', u'28'),
        (u'29', u'29'),
        (u'30', u'30'),
        (u'31', u'31'),
        )

_meses = (
        (u'1', u'Enero'),
        (u'2', u'Febrero'),
        (u'3', u'Marzo'),
        (u'4', u'Abril'),
        (u'5', u'Mayo'),
        (u'6', u'Junio'),
        (u'7', u'Julio'),
        (u'8', u'Agosto'),
        (u'9', u'Septiembre'),
        (u'10', u'Octubre'),
        (u'11', u'Noviembre'),
        (u'12', u'Diciembre'),
        )

_anos = (
        (u'2017', u'2017'),
        (u'2018', u'2018'),
        (u'2019', u'2019'),
        (u'2020', u'2020'),
        )

_hora = (
        (u'00', u'00'),
        (u'01', u'01'),
        (u'02', u'02'),
        (u'03', u'03'),
        (u'04', u'04'),
        (u'05', u'05'),
        (u'06', u'06'),
        (u'07', u'07'),
        (u'08', u'08'),
        (u'09', u'09'),
        (u'10', u'10'),
        (u'11', u'11'),
        (u'12', u'12'),
        (u'13', u'13'),
        (u'14', u'14'),
        (u'15', u'15'),
        (u'16', u'16'),
        (u'17', u'17'),
        (u'18', u'18'),
        (u'19', u'19'),
        (u'20', u'20'),
        (u'21', u'21'),
        (u'22', u'22'),
        (u'23', u'23'),
        )

_minutos = (
        (u'00', u'00'),
        (u'01', u'01'),
        (u'02', u'02'),
        (u'03', u'03'),
        (u'04', u'04'),
        (u'05', u'05'),
        (u'06', u'06'),
        (u'07', u'07'),
        (u'08', u'08'),
        (u'09', u'09'),
        (u'10', u'10'),
        (u'11', u'11'),
        (u'12', u'12'),
        (u'13', u'13'),
        (u'14', u'14'),
        (u'15', u'15'),
        (u'16', u'16'),
        (u'17', u'17'),
        (u'18', u'18'),
        (u'19', u'19'),
        (u'20', u'20'),
        (u'21', u'21'),
        (u'22', u'22'),
        (u'23', u'23'),
        (u'24', u'24'),
        (u'25', u'25'),
        (u'26', u'26'),
        (u'27', u'27'),
        (u'28', u'28'),
        (u'29', u'29'),
        (u'30', u'30'),
        (u'31', u'31'),
        (u'32', u'32'),
        (u'33', u'33'),
        (u'34', u'34'),
        (u'35', u'35'),
        (u'36', u'36'),
        (u'37', u'37'),
        (u'38', u'38'),
        (u'39', u'39'),
        (u'40', u'40'),
        (u'41', u'41'),
        (u'42', u'42'),
        (u'43', u'43'),
        (u'44', u'44'),
        (u'45', u'45'),
        (u'46', u'46'),
        (u'47', u'47'),
        (u'48', u'48'),
        (u'49', u'49'),
        (u'50', u'50'),
        (u'51', u'51'),
        (u'52', u'52'),
        (u'53', u'53'),
        (u'54', u'54'),
        (u'55', u'55'),
        (u'56', u'56'),
        (u'57', u'57'),
        (u'58', u'58'),
        (u'59', u'59'),
        )

BIRTH_YEAR_CHOICES = ('2015', '2016', '2017', '2018')

FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)

#modelo para el formulario el filtrado de busqueda de datos
class Busqueda(forms.Form):
    today = datetime.date.today()
    #hora inicio busqueda en formulario por defecto
    hora = '00'
    minut = '00'
    hora_fin = '23'
    minut_fin = '59'
    diaInicio = forms.ChoiceField(choices=_dias, initial=today.day, label='Fecha Inicio de Busqueda')
    mesInicio = forms.ChoiceField(choices=_meses, initial=today.month, label='')
    anoInicio = forms.ChoiceField(choices=_anos, initial=today.year,label='')
    diaFin = forms.ChoiceField(choices=_dias, initial=today.day, label='Fecha Fin de Busqueda')  #nombre para mostrar en el formulario
    mesFin = forms.ChoiceField(choices=_meses, initial=today.month, label='')
    anoFin = forms.ChoiceField(choices=_anos, initial=today.year, label='')
    horaInicio = forms.ChoiceField(choices=_hora, initial=hora, label='Desde la hora:')
    minutoInicio = forms.ChoiceField(choices=_minutos, initial=minut, label='')
    horaFin = forms.ChoiceField(choices=_hora, initial=hora_fin, label='Hasta la hora:')
    minutoFin = forms.ChoiceField(choices=_minutos, initial=minut_fin, label='')
    Distancia = forms.BooleanField(label='Distancia Recorrida en km', required=False, initial=False)

    #el help_text es texto al costado de ayuda
#    telefono = forms.CharField(initial='ingrese el abonado')  #declara valor inicial

#    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
#    favorite_colors = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple,choices=FAVORITE_COLORS_CHOICES,)
