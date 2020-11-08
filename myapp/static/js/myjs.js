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
    const catBags = document.querySelectorAll('.cat-bags')
    const nextBtn5 = document.getElementById('5');
    const checkboxes_radio = document.getElementsByName("organization");
    const address = document.getElementById("address")
    const city = document.getElementById("city")
    const postcode = document.getElementById("postcode")
    const phone = document.getElementById("phone")
    const data = document.getElementById("data")
    const time = document.getElementById("time")
    const com_c = document.getElementById("com_c")
    const data_spec = document.querySelectorAll(".data-spec")


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
        // let data_spec_list = []
        // for (var i = 0; i < data_spec.length; i++) {
        //     data_spec_list.push()
        // }
        // document.getElementById("tab-1")
    });
    });