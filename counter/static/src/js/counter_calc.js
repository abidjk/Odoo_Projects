/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import {Reset} from "./reset_calc"
// Define the Counter component
export class Counter extends Component {
    static template = "counter.counterClac";
    static components={...Counter,
    Reset}// The template that will represent this component
    setup() {
        this.state = useState({ value: 0 });  // Initialize counter state with value 0
    }
    // Increment method to increase the counter value
    increment() {
        this.state.value++;
    }
    decrement(){
        if(this.state.value != 0){
            this.state.value--;
        }
    }
    reset(){
       this.state.value = 0;
    }
}
registry.category("actions").add("Counter.counter", Counter);
