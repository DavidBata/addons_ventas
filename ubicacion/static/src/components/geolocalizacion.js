/** @odoo-module */

import { registry } from "@web/core/registry"
import { CharField } from "@web/views/fields/char/char_field"
import { standardFieldProps } from "@web/views/fields/standard_field_props";



const { Component, useSubEnv, useState,useRef } = owl


class UbicacionField extends Component {
    inputRef = useRef("input");
    
    setup(){
        
        super.setup()
        console.log("Otro Char Field Field Inherited")
        console.log(this.props)

        this.state = useState({  
                
                                           
            ubicacion_data: this.props.value ||'',
            
        })

       
        
         
      
        
        
    }

    
    focusInput() {
        
        this.inputRef.el.focus();
    }
  

    muestraMensaje(elemento) {

        
       
        const el = document.getElementById("customUbicacion1");       
        const cajatext = document.getElementById("customUbicacion");
        el.addEventListener(elemento,() => {
             
            console.log('entro');
            cajatext.focus();            
            console.log('probando clic');
        });
        
        
      }

      
   
 

    async ubicacionDomain(){        

        
        
                
            navigator.geolocation.getCurrentPosition(position => {
                const {latitude,longitude} = position.coords;                
                let cadena = `${latitude}, ${longitude}`;   
                console.log(cadena);        
               
                
                 this.state.ubicacion_data = cadena;
              
               
               
               
           
            });

           
          
      
       
       
      
         
     
    }

    

    
    
}


UbicacionField.template = "ubicacion.UbicacionField"

 
UbicacionField.supportedTypes = ["char"]

UbicacionField.props = {
    ...standardFieldProps,
};

registry.category("fields").add("ubicacion", UbicacionField)