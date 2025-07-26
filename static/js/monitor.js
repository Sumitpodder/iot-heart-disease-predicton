        const records = [];
        const healthForm = document.getElementById('healthForm');
        const recordsBody = document.getElementById('recordsBody');
        const editModal = document.getElementById('editModal');
        const editForm = document.getElementById('editForm');
        const closeModal = document.getElementById('closeModal');
        let editingId = null;

        healthForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const bp = document.getElementById('bp').value;
            const blood_sugar = document.getElementById('blood_sugar').value;
            const heart_rate = document.getElementById('heart_rate').value;
            const chest_pain = document.getElementById('chest_pain').value;
            const anxiety = document.getElementById('anxiety').value;
            const weakness = document.getElementById('weakness').value;

            const newRecord = {
                id: crypto.randomUUID(),
                bp,
                blood_sugar,
                heart_rate,
                chest_pain,
                anxiety,
                weakness,
                created_at: new Date().toISOString(),
                prediction: null
            };

            records.unshift(newRecord);
            renderRecords();
            healthForm.reset();
        });

        function renderRecords() {
            recordsBody.innerHTML = '';
            records.forEach(record => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${new Date(record.created_at).toLocaleString()}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.bp}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.blood_sugar}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.heart_rate}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.chest_pain}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.anxiety}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.weakness}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${record.prediction || 'Not Predicted'}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <button onclick="editRecord('${record.id}')" class="text-blue-600 hover:text-blue-900">Edit</button>
                        <button onclick="deleteRecord('${record.id}')" class="text-red-600 hover:text-red-900">Delete</button>
                        <button onclick="predictRecord('${record.id}')" class="text-purple-600 hover:text-purple-900">Predict</button>
                    </td>
                `;
                recordsBody.appendChild(row);
            });
        }

        function editRecord(id) {
            const record = records.find(r => r.id === id);
            if (record) {
                document.getElementById('edit_bp').value = record.bp;
                document.getElementById('edit_blood_sugar').value = record.blood_sugar;
                document.getElementById('edit_heart_rate').value = record.heart_rate;
                document.getElementById('edit_chest_pain').value = record.chest_pain;
                document.getElementById('edit_anxiety').value = record.anxiety;
                document.getElementById('edit_weakness').value = record.weakness;
                editingId = id;
                editModal.classList.remove('hidden');
            }
        }

        editForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const updatedRecord = {
                id: editingId,
                bp: document.getElementById('edit_bp').value,
                blood_sugar: document.getElementById('edit_blood_sugar').value,
                heart_rate: document.getElementById('edit_heart_rate').value,
                chest_pain: document.getElementById('edit_chest_pain').value,
                anxiety: document.getElementById('edit_anxiety').value,
                weakness: document.getElementById('edit_weakness').value,
                created_at: new Date().toISOString(),
                prediction: null
            };

            const index = records.findIndex(r => r.id === editingId);
            if (index > -1) {
                records[index] = updatedRecord;
                renderRecords();
                editModal.classList.add('hidden');
            }
        });

        closeModal.addEventListener('click', function () {
            editModal.classList.add('hidden');
        });

        function deleteRecord(id) {
            const index = records.findIndex(r => r.id === id);
            if (index > -1) {
                records.splice(index, 1);
                renderRecords();
            }
        }

        function predictRecord(id) {
            const predictions = ['Normal', 'Mild Risk', 'Moderate Risk', 'High Risk'];
            const randomPrediction = predictions[Math.floor(Math.random() * predictions.length)];
            const record = records.find(r => r.id === id);
            if (record) {
                record.prediction = randomPrediction;
                renderRecords();
            }
        }
