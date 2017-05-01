from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^derivadas', 'Tesis.views.derivadas'),
    url(r'^grafico1var', 'Tesis.views.grafico1var'),
    url(r'^grafico2var', 'Tesis.views.grafico2var'),
    url(r'^derivadaNumerica', 'Tesis.views.derivadaNumerica'),
    url(r'^der_numerica_ajax', 'Tesis.views.derivadaAjax'),
    url(r'^integralesDobles', 'Tesis.views.integralesDobles'),
    url(r'^integrales', 'Tesis.views.integrales'),
    url(r'^graficar$', 'Tesis.views.graficarFuncion_ajax'),
    url(r'^graficar3d$', 'Tesis.views.graficarFuncion3d_ajax'),
    url(r'^graficar_derivada$', 'Tesis.views.graficarDerivada_ajax'),
    url(r'^graficar_biseccion$', 'Tesis.views.graficarBiseccion_ajax'),
    url(r'^graficar_newton$', 'Tesis.views.graficarNewton_ajax'),
    url(r'^menu', 'Tesis.views.menu'),
    url(r'^$', 'Tesis.views.menu'),
    url(r'^biseccion', 'Tesis.views.biseccion'),
    url(r'^newton', 'Tesis.views.newton'),
)
