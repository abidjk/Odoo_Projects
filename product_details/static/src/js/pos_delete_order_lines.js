import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";
patch(ProductScreen.prototype, {
    async onClickDelete() {
        var lines = this.currentOrder.get_orderlines()
        lines.filter(line => line).forEach(line =>{
        this.currentOrder.removeOrderline(line)
        })
    },
});

patch(Orderline.prototype, {
   setup(){
    this.pos = usePos();
    return super.setup(...arguments)
   },
    removeOrderline(line){
        var order =  this.pos.get_order()
        let order_line = order.lines.find(item => item.id == line.id)
        if (order_line){
            order.removeOrderline(order_line)
        }
    }
})


