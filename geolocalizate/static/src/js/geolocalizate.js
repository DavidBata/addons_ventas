/** @odoo-module */

import { registry } from "@web/core/registry"

const { Component } = owl

export class Geolicalizate extends Component {

  setup() {
    console.log("Entering Geolicaliz")
  }
}
Geolicalizate.template="geolocalizate.Golocalizate"

registry.category("actions").add("geolocalizate.Golocalizate",Geolicalizate)
























// // import { memoize } from "@web/core/utils/functions";

// import { registry } from "./core/registry";

// const GeolocalizateJs = {
//     dependencies: ["notification"],
//     start(env, { notification }) {
//         let counter = 1;
//         setInterval(() => {
//             notification.add(`Tick Tock ${counter++}`);
//         }, 5000);
//     }
// };
// serviceRegistry.add("GeolocalizateJs", GeolocalizateJs);


// odoo.define('res.partner', function (require) {
//     "use strict";
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(showPosition);
//       } else {
//         //document.getElementById("demo").innerHTML =
//         console.log("Geolocation is not supported by this browser.");
//       }
//       function showPosition(position) {
//         // document.getElementById("demo").innerHTML =
//         // "Latitude: " + position.coords.latitude + "<br>" +
//         // "Longitude: " + position.coords.longitude;
//         var postion = position.coords.latitude + ',' + position.coords.longitude
//         console.log(postion)
//         return postion
//       }
// });
// showPosition.template = "geolocalizate.geolocalizate_template";

// registry.category("fields").add("sales_team_progressbar", SaleProgressBarField);
