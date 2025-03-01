/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size){
    const result = [];
    for (let i = 0;i < array.length; i += size){
        result.push(array.slice(i, i + size));
    }
    if(array.length != 0){
    array[0].is_active = true;
    }
    return result;
}
export function _generateRandomId(length = 4) {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
};
var SchoolEvents = PublicWidget.Widget.extend({
        selector: '.school_events_snippet',
        willStart: async function () {
            const data = await rpc('/school_events', {})
            const school_events = data
            Object.assign(this, {
                school_events
            })
        },
        start: function () {
            const refEl = this.$el.find("#top_products_carousel")
            const school_events_display = this.school_events
            const chunkData = _chunk(school_events_display, 4)
            const slide_id = _generateRandomId()
            var template= renderToElement('school.school_events_snippet_view',{
                school_events_display,
                chunkData,
                slide_id
            })
            refEl.html(template)
        }
    });
PublicWidget.registry.school_events = SchoolEvents;
return SchoolEvents;