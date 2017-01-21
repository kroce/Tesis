from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^derivadas', 'Tesis.views.derivadas'),
    url(r'^derivadaNumerica', 'Tesis.views.derivadaNumerica'),
    url(r'^der_numerica_ajax', 'Tesis.views.derivadaAjax'),
    url(r'^integralesDobles', 'Tesis.views.integralesDobles'),
    url(r'^integrales', 'Tesis.views.integrales'),
    url(r'^graficar$', 'Tesis.views.graficarFuncion_ajax'),
    url(r'^graficar3d$', 'Tesis.views.graficarFuncion3d_ajax'),
    url(r'^graficar_derivada$', 'Tesis.views.graficarDerivada_ajax'),
    url(r'^graficar_biseccion$', 'Tesis.views.graficarBiseccion_ajax'),
    url(r'^menu', 'Tesis.views.menu'),
   # url(r'^ajaxexample$', 'Tesis.views.main'),
    #url(r'^ajaxexample_json$', 'Tesis.views.ajax'),
    url(r'^biseccion', 'Tesis.views.biseccion'),
    #url(r'^prueba', 'Tesis.views.prueba'),
    #url(r'^create_post', 'Tesis.views.pruebaAjax'),
)
