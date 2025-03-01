/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";
publicWidget.registry.MaterialRequest = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'change #student_id': '_onChangeStudent',
       'change #start_date,#end_date': '_onChangeStartdate',
       'change #club_ids': '_onChangeClubids',
       'change #dob': '_onChangeDob',
   },
   _onChangeStudent: function(ev){
           var student = parseInt(this.$el.find('#student_id').val())
            if(student != ""){
            rpc('/get/class',{action:student}).then(res =>{
                  this.$el.find('#class_name').val(res['class_name'])
                  this.$el.find('#class_id').val(res['class_id'])
                })
            }
           },
   _onChangeStartdate: function(ev){
    var start_date = new Date(this.$el.find('#start_date').val())
    var end_date = new Date(this.$el.find('#end_date').val())
    if (!isNaN(start_date) && !isNaN(end_date)){
        if(end_date >= start_date){
            var tot_days = 0
            var currentDate = new Date(start_date);
            while(currentDate <= end_date){
             var dayOfWeek = currentDate.getDay();
             if(dayOfWeek != 0 && dayOfWeek != 6){
                tot_days++
             }
             currentDate.setDate(currentDate.getDate()+1);
            }
            this.$el.find('#total_days').val(tot_days)
        }else{
            alert("End date should be greater than start date")
        }
    }
   },
   _onChangeDob: function(ev){
    var dob = new Date(this.$el.find('#dob').val())
    var now = new Date()
    var five_years_ago = new Date(now.getFullYear()-5,now.getMonth(),now.getDay());
    if (dob < five_years_ago){
    var difference = Math.round((now - dob)/(1000*60*60*24*365))
    this.$el.find('#age').val(difference)
    }else{
        alert("Age must be more than 5")
    }
   },
    _onChangeClubids: function(ev){
    var selectedClubs = this.$el.find('#club_ids').val() || []
        rpc('/get-clubs',{clubs : selectedClubs}).then(res =>{
                  this.$el.find('#selected_club_ids').val(res['club_ids'])
                })
    }
   })
