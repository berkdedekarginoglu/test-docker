let get_data = function() {
   fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/agents")
   .then(function(response){
      return response.json();
   })
   .then(function(agents){
      let data_output_scan_flow = document.querySelector("#data-output-scan-flow");
      let scan_out = "";

      for(let agent of agents){
         scan_out += `
            <tr>
               <td class="text-center">${agent.agent}</td>
               <td class="text-center">${agent.success_rate.split('.')[0]}</td>
               <td class="text-center">${agent.success}</td>
               <td class="text-center">${agent.password_change_errors}</td>
               <td class="text-center">${agent.current_step}</td>
               <td class="text-center">${agent.scan_range}</td>
               <td class="text-center">+${agent.country_code}</td>
               <td class="text-center">${agent.gsm_code}</td>
               <td class="text-center">${agent.gsm_errors} sec</td>
               <td class="text-center">${agent.password_errors}</td>
            </tr>
         `;
      };
   
      data_output_scan_flow.innerHTML = scan_out;
   });
}

get_data();

setInterval(function() {
  get_data();
 }, 10000);