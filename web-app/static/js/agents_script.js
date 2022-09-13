agent_data = []
let create_data = async function() {
   fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/agents/scans")
   .then(function(response){
      return response.json();
   })
   .then(function(agents){
      let data_output_scan_flow = document.querySelector("#data-output-scan-flow");
      let scan_out = "";
      let sortedInput = agents.slice().sort((a, b) => parseInt(b.success) - parseInt(a.success));
      for(let agent of sortedInput){
         
         if(agent_data.some(item => item.country_code === agent.country_code &&
            item.gsm_code === agent.gsm_code && item.current_step == agent.current_step)){
               continue;
            }
         
         var tr = document.createElement('tr');
         var td1 = document.createElement('td').className("text-center");
         var td2 = document.createElement('td').className("text-center");
         var td3 = document.createElement('td').className("text-center");
         var td4 = document.createElement('td').className("text-center");
         var td5 = document.createElement('td').className("text-center");
         var td6 = document.createElement('td').className("text-center");
         var td7 = document.createElement('td').className("text-center");
         var td8 = document.createElement('td').className("text-center");
         var td9 = document.createElement('td').className("text-center");
         var td10 = document.createElement('td').className("text-center");
         
         td1.className("text-center");
         td2.className("text-center");
         td3.className("text-center");
         td4.className("text-center");
         td5.className("text-center");
         td6.className("text-center");
         td7.className("text-center");
         td8.className("text-center");
         td9.className("text-center");
         td10.className("text-center");

         var text1 = document.createTextNode(agent.agent);
         var text2 = document.createTextNode(agent.success_rate.split('.')[0]);
         var text3 = document.createTextNode(agent.success);
         var text4 = document.createTextNode(agent.password_change_errors);
         var text5 = document.createTextNode(agent.current_step);
         var text6 = document.createTextNode(agent.scan_range);
         var text7 = document.createTextNode(agent.country_code);
         var text8 = document.createTextNode(agent.gsm_code);
         var text9 = document.createTextNode(agent.gsm_errors);
         var text10 = document.createTextNode(agent.password_errors);
         
         td1.appendChild(text1);
         td2.appendChild(text2);
         td3.appendChild(text3);
         td4.appendChild(text4);
         td5.appendChild(text5);
         td6.appendChild(text6);
         td7.appendChild(text7);
         td8.appendChild(text8);
         td9.appendChild(text9);
         td10.appendChild(text10);

         tr.appendChild(td1);
         tr.appendChild(td2);
         tr.appendChild(td3);
         tr.appendChild(td4);
         tr.appendChild(td5);
         tr.appendChild(td6);
         tr.appendChild(td7);
         tr.appendChild(td8);
         tr.appendChild(td9);
         tr.appendChild(td10);

      };
   });
}


let data_filter = function() {
   var input, filter, table, tr, td, i, txtValue;
   if(input){
   filter = document.getElementById("agent_scan_flow_table_filter");
   table = document.getElementById("agent_scan_flow_table");
   tr = table.getElementsByTagName("tr");
   for (i = 0; i < tr.length; i++) {
     td = tr[i].getElementsByTagName("td")[6];
     if (td) {
       txtValue = td.textContent || td.innerText;
       if (txtValue.indexOf(filter) > -1) {
         tr[i].style.display = "";
       } else {
         tr[i].style.display = "none";
       }
     }       
   }
 }
}

let get_stats = function() {
   fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/agents/stats")
   .then(function(response){
      return response.json();
   })
   .then(function(agents){
      let data_output_stats_flow = document.querySelector("#data-output-stats-flow");
      let stats_out = "";

      for(let agent of agents){
         stats_out += `
            <tr>
               <td class="text-center">${agent.agent}</td>
               <td class="text-center">${agent.last_info.split('.')[0]}</td>
               <td class="text-center">${agent.current_country}</td>
               <td class="text-center">${agent.current_gsm}</td>
               <td class="text-center">${agent.current_step}</td>
            </tr>
         `;
      };
   
      data_output_stats_flow.innerHTML = stats_out;
   });
}

get_stats();
create_data();

setInterval(function() {
   get_stats();
   create_data();
 }, 10000);