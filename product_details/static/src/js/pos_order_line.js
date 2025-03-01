import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup(vals) {
        this.description = this.product_id.description || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
        return {
            description: this.get_product().description || "",
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
                description: { type: String, optional: true},
            },
        },
    },
});


