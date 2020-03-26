function createCalendar(year, month){
	let weekdays = ["mon", "tue", "wen", "thu", "fri", "sat", "sun"]
	let date = new Date(year, month)
  let table = document.createElement("table")
	document.body.append(table);
  let tr = document.createElement("tr")
	table.insertAdjacentElement("beforeend", tr);
	//Main th with weekdays
	for(let i=0; i<7; i++){
		tr.insertAdjacentHTML("beforeend", `<th>${weekdays[i]}</th>`);
	}
	//Main filling in cycle
	for (let i=0; date.getMonth() == month; i++){
		if (i%7==0 || i==0){ //if i==7, meaning 7days passed by and a new line is needed; i==0, a new line is needed to devide from th weekdays
			let tr = document.createElement("tr")
			table.insertAdjacentElement("beforeend", tr)
		}
		if (i<date.getDay()-1){ //empty tds at the beginning of the month
			table.lastElementChild.insertAdjacentHTML("beforeend", `<td></td>`)
			continue;
		}else if (date.getDay()==i && i==0){ //sunday, 6 empty squares
			let counter=0
			while(counter<6){
				table.lastElementChild.insertAdjacentHTML("beforeend", `<td></td>`)
				counter++
			}
			i=6
		}
		table.lastElementChild.insertAdjacentHTML("beforeend", `<td>${date.getDate()}</td>`)
		date.setDate(date.getDate()+1)
  }
  
  return table
}

function styling(){
	let table = document.body.querySelector(".calendar table");
	let date = new Date()
	let today;
	let tds = document.body.querySelectorAll(".calendar table td")

	for (td of tds){ //single out the current date
		if (td.innerText == date.getDate()){
			today=td
			td.style.backgroundColor = "#ffa600"
			td.style.color = "white"
		}
	}
}

let div = document.body.querySelector(".calendar")
let currentDate = new Date()
let currentYear = currentDate.getFullYear()
let currentMonth = currentDate.getMonth()


div.append(createCalendar(currentYear, currentMonth))
styling()



