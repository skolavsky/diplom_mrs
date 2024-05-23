const modal = document.getElementById('modal');
const modalBody = document.getElementById('modal-body');
const closeButton = document.querySelector('.close-button');
const clientTableWrapper = document.getElementById('clientTableWrapper');

clientTableWrapper.addEventListener('click', function (event) {
    if (event.target.classList.contains('show-spoiler-button')) {
        const clientUrl = event.target.getAttribute('data-client-url');

        fetch(clientUrl)
            .then(response => response.text())
            .then(data => {
                modalBody.innerHTML = data;
                modal.style.display = 'block';

                // Добавляем обработчики событий после загрузки формы
                const spo2Input = modalBody.querySelector('[name="spo2"]');
                const oxygenFlowInput = modalBody.querySelector('[name="oxygen_flow"]');
                const chdInput = modalBody.querySelector('[name="ch_d"]');
                const roxInput = modalBody.querySelector('[name="rox"]');
                const spo2FioInput = modalBody.querySelector('[name="spo2_fio"]');
                const mvvInput = modalBody.querySelector('[name="mvv"]');
                const mvInput = modalBody.querySelector('[name="mv"]');
                const ventilationReserveInput = modalBody.querySelector('[name="ventilation_reserve"]');
                const editClientForm = modalBody.querySelector('form');

                if (spo2Input && oxygenFlowInput && chdInput && roxInput && spo2FioInput && mvvInput && mvInput && ventilationReserveInput && editClientForm) {
                    let timeoutId;
                    let prevSpo2Fio = parseFloat(spo2FioInput.value);
                    let prevRox = parseFloat(roxInput.value);
                    let prevVentilationReserve = parseFloat(ventilationReserveInput.value);

                    function calculateValues() {
                        const spo2 = parseFloat(spo2Input.value);
                        const oxygenFlow = parseFloat(oxygenFlowInput.value);
                        const chd = parseFloat(chdInput.value);
                        const mvv = parseFloat(mvvInput.value);
                        const mv = parseFloat(mvInput.value);

                        // Calculate SPO2/FIO
                        let spo2Fio = null;
                        if (!isNaN(spo2) && !isNaN(oxygenFlow)) {
                            spo2Fio = (spo2 / ((21 + 3 * oxygenFlow) / 100)).toFixed(3);
                            if (spo2Fio !== prevSpo2Fio) {
                                spo2FioInput.value = spo2Fio;
                                addHighlight(spo2FioInput);
                                prevSpo2Fio = spo2Fio; // Обновляем предыдущее значение
                            }
                        } else {
                            spo2FioInput.value = '';
                        }

                        // Calculate ROX
                        let rox = null;
                        if (!isNaN(spo2Fio) && !isNaN(chd) && chd !== 0) {
                            rox = (spo2Fio / chd).toFixed(3);
                            if (rox !== prevRox) {
                                roxInput.value = rox;
                                addHighlight(roxInput);
                                prevRox = rox; // Обновляем предыдущее значение
                            }
                        } else {
                            roxInput.value = '';
                        }

                        // Calculate Ventilation Reserve
                        let ventilationReserve = null;
                        if (!isNaN(mvv) && !isNaN(mv) && mv !== 0) {
                            ventilationReserve = (mvv / mv).toFixed(3);
                            if (ventilationReserve !== prevVentilationReserve) {
                                ventilationReserveInput.value = ventilationReserve;
                                addHighlight(ventilationReserveInput);
                                prevVentilationReserve = ventilationReserve; // Обновляем предыдущее значение
                            }
                        } else {
                            ventilationReserveInput.value = '';
                        }
                    }

                    function delayedCalculateValues() {
                        clearTimeout(timeoutId);
                        timeoutId = setTimeout(calculateValues, 1500); // 3 секунды задержки
                    }

                    function addHighlight(element) {
                        element.classList.add('highlight');
                        setTimeout(() => {
                            element.classList.remove('highlight');
                        }, 1000); // Убираем класс через 1 секунду
                    }

                    spo2Input.addEventListener('input', delayedCalculateValues);
                    oxygenFlowInput.addEventListener('input', delayedCalculateValues);
                    chdInput.addEventListener('input', delayedCalculateValues);
                    mvvInput.addEventListener('input', delayedCalculateValues);
                    mvInput.addEventListener('input', delayedCalculateValues);

                    editClientForm.addEventListener('submit', function (event) {
                        // Удаляем значения rox и spo2_fio и ventilation_reserve перед отправкой формы
                        roxInput.disabled = true;
                        spo2FioInput.disabled = true;
                        ventilationReserveInput.disabled = true;
                    });
                } else {
                    console.error('Не удалось найти элементы формы. Проверьте правильность идентификаторов.');
                }
            })
            .catch(error => console.error('Error:', error));
    }
});

if (closeButton) {
    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}