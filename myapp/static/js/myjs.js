document.addEventListener("DOMContentLoaded", function () {
    const nextBtn = document.getElementById('1');
    const inst = document.querySelectorAll('.filter-inst');
    const checkboxes = document.getElementsByName('categories');

    function addHide(element) {
        console.log('test2')
        for (var i = 0; i < inst.length; i++) {
            if (inst[i].classList.contains(element) == false) {
                console.log('test3')
                inst[i].classList.add('hide');
            }
            console.log('test4')
        }
    }

    nextBtn.addEventListener('click', function () {
        const selected = [];
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                selected.push(checkboxes[i].value);
            }
        }

        selected.forEach(addHide)


    });
    const bagsNumber = document.getElementById("bags");
    const nextBtn5 = document.getElementById('5');
    const checkboxes_radio = document.getElementsByName("organization");
    const data_spec = document.querySelectorAll(".data-spec")
    const data_spec2 = document.querySelectorAll(".data-spec2")
    nextBtn5.addEventListener('click', function () {
        let selected_text = "";
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                selected_text = selected_text + checkboxes[i].nextElementSibling.nextElementSibling.textContent + ", ";

            }
        }
        for (var i = 0; i < checkboxes_radio.length; i++) {
                    if (checkboxes_radio[i].checked) {
                document.getElementById("inst-sum").textContent = "Dla " + checkboxes_radio[i].nextElementSibling.nextElementSibling.firstElementChild.textContent

            }
                    }
        document.getElementById("bags-sum").textContent = bagsNumber.value + " worków - " + selected_text
        let data_string = ""
        for (var i = 0; i < data_spec.length; i++) {
            data_string = data_string + "<li>" + data_spec[i].value + "</li>"
        }
        document.getElementById("tab-1").outerHTML = "<ul>" + data_string + "</ul>"
                let data_string2 = ""
        for (var i = 0; i < data_spec2.length; i++) {
            data_string2 = data_string2 + "<li>" + data_spec2[i].value + "</li>"
        }
        document.getElementById("tab-2").outerHTML = "<ul>" + data_string2 + "</ul>"
    });

    });