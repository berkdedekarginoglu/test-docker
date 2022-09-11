setInterval(function() {
   fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/workers")
.then(function(response){
   return response.json();
})
.then(function(workers){
   let data_output_rate_flow = document.querySelector("#data-output-rate-flow");
   let rate_out = "";
   let error_output_rate_flow = document.querySelector("#data-output-error-flow");
   let error_out = "";
   let total_success = 0
   let total_scan = 0
   for(let worker of workers){
      total_success = total_success + parseInt(worker.total_success)
      total_scan = total_scan + parseInt(worker.total_scan)
      rate_out += `
         <tr>
            <td class="text-center">${worker.worker_ip}</td>
            <td class="text-center">${worker.total_scan}</td>
            <td class="text-center">${worker.total_success}</td>
            <td class="text-center">${worker.last_success_date.split('.')[0]}</td>
            <td class="text-center">${worker.success_rate.split('.')[0]}</td>
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

         rate_out += `
         <tr>
            <td class="text-center"><b>Total</b></td>
            <td class="text-center">${total_scan}</td>
            <td class="text-center">${total_success}</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
            <td class="text-center">-</td>
         </tr>
      `;

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
 }, 10000);