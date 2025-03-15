import { Component } from "@odoo/owl";

export class Reset extends Component {
    static template = "counter.ResetButton";
//    static components = { ...GraphController.components, HrActionHelper };
    static props = {
        onClick: { type: Function, optional: true },
    };
}