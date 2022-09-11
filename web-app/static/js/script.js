fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/workers")
.then(function(response){
   return response.json();
})
.then(function(workers){
   let data_output_rate_flow = document.querySelector("#data-output-rate-flow");
   let rate_out = "";
   let error_output_rate_flow = document.querySelector("#data-output-error-flow");
   let error_out = "";
   for(let worker of workers){
      rate_out += `
         <tr>
            <td class="text-center">${worker.worker_ip}</td>
            <td class="text-center">${worker.total_scan}</td>
            <td class="text-center">${worker.total_success}</td>
            <td class="text-center">${worker.last_success_date}</td>
            <td class="text-center">${worker.success_rate}</td>
            <td class="text-center">${worker.success}</td>
            <td class="text-center">+${worker.selected_country}</td>
            <td class="text-center">${worker.selected_gsm}</td>
            <td class="text-center">${worker.round_time.split('.')[0]} sec</td>
            <td class="text-center">${worker.current_step}</td>
            <td class="text-center">${worker.proxy_host}</td>
            <td class="text-center">${worker.proxy_port}</td>
         </tr>
      `;
   };

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
 
   data_output_rate_flow.innerHTML = rate_out;
   error_output_rate_flow.innerHTML = error_out;
});