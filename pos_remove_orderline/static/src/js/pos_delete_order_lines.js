import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
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

patch(PosOrderline.prototype, {
    getDisplayData() {
        return {
            id: this.id,
            ...super.getDisplayData(),
        };
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                id: { type: String, optional: true},
            },
        },
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
});


