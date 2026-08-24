function loadFirebase() {
    var script1 = document.createElement('script');
    script1.src = "https://gstatic.com";
    var script2 = document.createElement('script');
    script2.src = "https://gstatic.com";
    
    script1.onload = function() {
        document.head.appendChild(script2);
    };
    script2.onload = function() {
        startSync();
    };
    document.head.appendChild(script1);
}

function startSync() {
    const firebaseConfig = {
        apiKey: "AIzaSyD8zsFJMsqNpCu491-GAzByQ8dqTZBqHew",
        authDomain: "://firebaseapp.com",
        databaseURL: "https://firebaseio.com",
        projectId: "nhat-ky-di-lam",
        storageBucket: "nhat-ky-di-lam.firebasestorage.app",
        messagingSenderId: "123680164523",
        appId: "1:123680164523:web:be4fcdb5e1118780ae85ee",
        measurementId: "G-GNRPY00TMV"
    };
  
    firebase.initializeApp(firebaseConfig);
    const database = firebase.database();

    // 1. TỰ ĐỘNG TẢI DỮ LIỆU VỀ MÀN HÌNH (Cả ĐT và Máy tính)
    database.ref('dulieu_nhatky/').on('value', (snapshot) => {
        const data = snapshot.val();
        if (data) {
           console.log("Đã đồng bộ dữ liệu mới nhất!");
           const inputs = document.querySelectorAll('input, textarea, select');
           inputs.forEach(input => {
               let key = input.id || input.name;
               if(key && data[key] !== undefined) {
                   if (input.type === 'checkbox') {
                       input.checked = data[key];
                   } else {
                       input.value = data[key];
                   }
               }
           });
        }
    });

    // 2. BỘ NÃO TỰ ĐỘNG: Bất kể bạn bấm vào nút "Ghi nhận" nào, cứ có nút bấm là tự lưu lên mạng!
    document.addEventListener('click', function(e) {
        // Nếu bấm vào bất kỳ nút bấm hoặc thẻ liên kết nào trên trang web
        if (e.target.closest('button') || e.target.closest('a')) {
            setTimeout(() => {
                let dataToSave = {};
                const inputs = document.querySelectorAll('input, textarea, select');
                
                inputs.forEach(input => {
                    let key = input.id || input.name;
                    if (key) {
                        dataToSave[key] = input.type === 'checkbox' ? input.checked : input.value;
                    }
                });
                
                // Đẩy toàn bộ các ô nhập liệu lên mạng cùng một lúc
                database.ref('dulieu_nhatky/').update(dataToSave);
                console.log("Đã tự động lưu dữ liệu sau khi bấm nút!");
            }, 200); // Đợi giao diện xử lý xong rồi lưu ngầm lên mạng
        }
    });
}

window.addEventListener('DOMContentLoaded', loadFirebase);
