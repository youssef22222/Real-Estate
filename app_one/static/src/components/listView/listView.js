/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class ListViewAction extends Component {
    static template = "app_one.ListView";

    setup(){
      this.state = useState({
          "records" : []
      });
      this.orm = useService("orm");
      this.rpc = useService("rpc");
      this.loadRecords();

      // this.loadRecords() method will be called each 3 seconds to update the state automatically in real-time
      this.intervalId = setInterval(() => {this.loadRecords();}, 3000);
      // once you close or leave you page(component) this line will be executed to avoid Error: Component is destroyed
      onWillUnmount(() => {clearInterval(this.intervalId);});

    };


    // async loadRecords(){
    //     const result = await this.orm.searchRead("property",[],[]);
    //     //[],[] => domain and fields names to get
    //     console.log(result);
    //     this.state.records = result;
    // };

       async loadRecords(){
           const result = await this.rpc("/web/dataset/call_kw/",{
               model : "property",
               method : "search_read",
               args : [[]], //search domain
               kwargs : {fields:["id", "name", "postcode", "date_availability"]} //get only this fields
           });
           console.log(result);
           this.state.records = result;
       };
}

registry.category("actions").add("app_one.action_list_view",ListViewAction);