bandits_analytics = []
var table = document.getElementById("bandit-table");
table.innerHTML = "";

let get_data = function() {
   fetch("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/bandits")
   .then(function(response){
      return response.json();
   })
   .then(function(bandits){
      let bandits_analytics_live_table = document.querySelector("#bandits-analytics-live");

      for(let bandit of bandits){
         
         if(bandits_analytics.some(obj => obj.worker_ip === bandit.worker_ip)){
            
         }

         var tr = document.createElement('tr');
         tr.setAttribute("role", "row");

         if(evenorodd===0){
            tr.classList.add("even");
            evenorodd = evenorodd + 1;
         }
         else{
            tr.classList.add("odd");
            evenorodd = 0;
         }

         var td1 = document.createElement('td');
         var td2 = document.createElement('td');
         var td3 = document.createElement('td');
         var td4 = document.createElement('td');
         var td5 = document.createElement('td');
         var td6 = document.createElement('td');
         var td7 = document.createElement('td');
         var td8 = document.createElement('td');
         var td9 = document.createElement('td');
         var td10 = document.createElement('td');
         var td11 = document.createElement('td');
         
         td1.setAttribute("class", "sorting_1 dtr-control");
         td2.setAttribute("class", "sorting_1 dtr-control");
         td3.setAttribute("class", "sorting_1 dtr-control");
         td4.setAttribute("class", "sorting_1 dtr-control");
         td5.setAttribute("class", "sorting_1 dtr-control");
         td6.setAttribute("class", "sorting_1 dtr-control");
         td7.setAttribute("class", "sorting_1 dtr-control");
         td8.setAttribute("class", "sorting_1 dtr-control");
         td9.setAttribute("class", "sorting_1 dtr-control");
         td10.setAttribute("class", "sorting_1 dtr-control");
         td11.setAttribute("class", "sorting_1 dtr-control");


         var text1 = document.createTextNode(bandit.worker_ip);
         var text2 = document.createTextNode(bandit.total_scan);
         var text3 = document.createTextNode(bandit.total_success);
         var text4 = document.createTextNode(bandit.last_success_date);
         var text5 = document.createTextNode(bandit.success_rate);
         var text6 = document.createTextNode(bandit.success);
         var text7 = document.createTextNode(bandit.selected_country);
         var text8 = document.createTextNode(bandit.selected_gsm);
         var text9 = document.createTextNode(bandit.round_time);
         var text10 = document.createTextNode(bandit.current_step);
         var text11 = document.createTextNode(bandit.proxy_host);
         
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
         td11.appendChild(text11);

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
         tr.appendChild(td11);

         bandits_analytics_live_table.appendChild(tr);

      };
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