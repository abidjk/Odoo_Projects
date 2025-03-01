import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";
patch(ProductScreen.prototype, {
    async onClickDelete() {
        var lines = this.currentOrder.get_orderlines()
        lines.filter(line => line).forEach(line => this.currentOrder.removeOrderline(line))
    },
});

patch(Orderline.prototype, {
   setup(){
    this.pos = usePos();
    return super.setup(...arguments)
   },
    async onClickRemove(){
//        var lines = this.pos.get_order().lines
//        lines.filter(line => line.full_product_name == this.props.line.productName).forEach(line => this.pos.get_order().removeOrderline(line))
//        console.log(line)

       var line = this.pos.get_order().lines.filter((line) => line.full_product_name == this.props.line.productName)[0]
       this.pos.get_order().removeOrderline(line)
//       this.pos.get_order().select_orderline(this.pos.get_order().lines[2])
       console.log(this.pos.get_order().get_last_orderline())
    }
})

//const line = order.lines.find(line => {
//    return line.product.display_name === this.props.line.productName;  // Alternative check
//});



//patch(Orderline.prototype, {
//    setup() {
//        this.pos = usePos();
//        super.setup();  // No need to pass arguments
//    },
//    async onClickRemove() {
//        const order = this.pos.get_order();
//        const line = order.lines.find(line => {
//            return line.full_product_name === this.props.line.productName;  // Alternative check
//        });
//
//        if (line) {
//            order.removeOrderline(line);
//        } else {
//            console.warn("Product not found in order lines.");
//        }
//    }
//});
