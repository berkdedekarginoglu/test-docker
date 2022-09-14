let get_data = function() {
   fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/api/bandits/statistics?limit=105&skip=0")
   .then(function(response){
     return response.json();

   })
   .then(function(bandits){
      console.log(bandits["data"]);
      let bandits_analytics_live_table = document.querySelector("#bandits-analytics-live");
      let evenorodd = 0;
      var outData = '';

      for(let bandit of bandits["data"]){


         outData += `
         <tr role="row" class="odd">
         <td class="dtr-control sorting_1" tabindex="0">${bandit.bandit}</td>
         <td class="sorting_1" tabindex="0">${bandit.total_scan}</td>
         <td class="sorting_1" tabindex="0">${bandit.total_success}}</td>
         <td class="sorting_1" tabindex="0">${bandit.last_success_date}</td>
         <td class="sorting_1" tabindex="0">${bandit.success_rate}</td>
         <td class="sorting_1" tabindex="0">${bandit.success}</td>
         <td class="sorting_1" tabindex="0">${bandit.selected_country}</td>
         <td class="sorting_1" tabindex="0">${bandit.selected_gsm}</td>
         <td class="sorting_1" tabindex="0">${bandit.round_time}</td>
         <td class="sorting_1" tabindex="0">${bandit.current_step}</td>
         <td class="sorting_1" tabindex="0">${bandit.proxy_host}</td>
         </tr>
         `
         
      }

      bandits_analytics_live_table.innerHTML = outData;
      
      /*
      for(let worker of workers){
         error_out += `
            <tr>
               <td class="text-center">${worker.worker_ip}</td>
               <td class="text-center">${worker.guest_token_errors}</td>
               <td class="text-center">${worker.login_flow_errors}</td>
               <td class="text-center">${worker.username_errors}</td>
               <td class="text-center">${worker.password_errors}</td>
               <td class="text-center">${worker.acid_flow_errors}</td>
               <td class="text-center">${worker.access_token_errors}</td>
               <td class="text-center">${worker.password_change_errors}</td>
               <td class="text-center">${worker.proxy_errors}</td>
               <td class="text-center">${worker.exceptions}</td>
            </tr>
         `;
      };
      */
      //error_output_rate_flow.innerHTML = error_out;
   });
}

get_data();

setInterval(function() {
  get_data();
 }, 10000);