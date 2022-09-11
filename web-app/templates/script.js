fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/workers")
.then(function(response){
   return response.json();
})
.then(function(products){
   let placeholder = document.querySelector("#data-output");
   let out = "";
   for(let worker of workers){
      out += `
         <tr>
            <td>${worker.worker_ip}</td>
            <td>${worker.total_success}</td>
            <td>${worker.total_scan}</td>
            <td>${worker.last_success_date}</td>
            <td>${worker.success_rate}</td>
            <td>${worker.success}</td>
            <td>${worker.selected_country}</td>
            <td>${worker.selected_gsm}</td>
            <td>${worker.round_time}</td>
            <td>${worker.current_step}</td>
            <td>${worker.fail_attemps}</td>
            <td>${worker.proxy_host}</td>
            <td>${worker.proxy_port}</td>
            <td>${worker.guest_token_errors}</td>
            <td>${worker.login_flow_errors}</td>
            <td>${worker.username_errors}</td>
            <td>${worker.password_errors}</td>
            <td>${worker.acid_flow_errors}</td>
            <td>${worker.access_token_errors}</td>
            <td>${worker.password_change_errors}</td>
            <td>${worker.proxy_errors}</td>
            <td>${worker.exceptions}</td>
         </tr>
      `;
   }
 
   placeholder.innerHTML = out;
});