/** @odoo-module */

import { registry } from "@web/core/registry"
import { formView } from "@web/views/form/form_view"
import { FormController } from "@web/views/form/form_controller"
import {orm_service} from '@web/core/orm_service'
import { useService } from "@web/core/utils/hooks"
import fieldRegistry from 'web.field_registry';
import { FieldChar } from 'web.basic_fields';

class ResPartnerFormController extends FormController {
    setup(){
        super.setup()
        this.rpc = useService("rpc");
        this.orm = useService("orm");
        console.log("This is res partner form controller")
        // var  ubicacion_data = null
        // this.action = useService("action")
        
    }
 
  ubicacionDomain(id){
    navigator.geolocation.getCurrentPosition(position => {
        const {latitude,longitude} = position.coords;
          let cadena = `latitud: ${latitude}: longitud: ${longitude}`;
         var  ubicacion_data= cadena;
          console.log(ubicacion_data);
          var rpc = require('web.rpc')
          var metodo =`geolocalizateme(${ubicacion_data})`
          // orm_service._rpcService
          
          rpc.query({ 
            model: 'res.partner', 
            method: "geolocalizateme",
            args: [[id],[ubicacion_data]], 
          }).then(function (datos) {
            if (datos=="ok") {
              console.log(datos)
              window.location.reload()
            }
            

          }).catch( function (err) {console.log(err)}); 
          
        }); 
    
      }
  
 }

ResPartnerFormController.template = "geolocalizate.ResPartnerFormView"

export const resPartnerFormView = {
    ...formView,
    Controller: ResPartnerFormController,
}

registry.category("views").add("res_partner_form_view", resPartnerFormView)