/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import { useState } from "@odoo/owl";
class SystrayIcon extends Component {
   setup() {
       super.setup(...arguments);
       this.state = useState({text : "", qrcode: ""})
   }
    _resetTextBox(){
        this.state.text = "";
        this.state.qrcode = "";
    }
    _generateQr(){
           var text = this.state.text.trim()
            if(text != ""){
            rpc('/get/qr',{text:text}).then(res =>{
                    this.state.qrcode = res['qr_image']
                })
            }
           }

}
   SystrayIcon.template = "qr_code_generator";
   SystrayIcon.components = {Dropdown, DropdownItem };
   export const systrayItem = { Component: SystrayIcon,};
   registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
