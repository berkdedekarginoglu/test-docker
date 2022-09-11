fetch("static/js/test.json")
.then(function(response){
   return response.json();
})
.then(function(workers){
   let placeholder = document.querySelector("#data-output");
   let out = "";
   for(let worker of workers){
      out += `
         <tr>
            <td>${worker.worker_ip}</td>
            <td>${worker.total_success}</td>
            <td>${worker.total_scan}</td>
            <td>${worker.success_rate}</td>
            <td>${worker.success}</td>
            <td>${worker.selected_country}</td>
            <td>${worker.selected_gsm}</td>
            <td>${worker.round_time}</td>
            <td>${worker.current_step}</td>
            <td>${worker.proxy.proxy_host}</td>
            <td>${worker.proxy.proxy_port}</td>
         </tr>
      `;
   }
 
   placeholder.innerHTML = out;
});