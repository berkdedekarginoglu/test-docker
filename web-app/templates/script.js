fetch("http://0.0.0.0:5000/workers")
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
            <td>${worker.proxy.host}</td>
            <td>${worker.proxy.port}</td>
            <td>${worker.errors.guest_token_errors}</td>
            <td>${worker.errors.login_flow_errors}</td>
            <td>${worker.errors.username_errors}</td>
            <td>${worker.errors.password_errors}</td>
            <td>${worker.errors.acid_flow_errors}</td>
            <td>${worker.errors.access_token_errors}</td>
            <td>${worker.errors.password_change_errors}</td>
            <td>${worker.errors.proxy_errors}</td>
            <td>${worker.errors.exceptions}</td>
         </tr>
      `;
   }
 
   placeholder.innerHTML = out;
});