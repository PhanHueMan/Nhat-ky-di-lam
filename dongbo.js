// Tải thư viện Firebase hỗ trợ đồng bộ ngầm bằng cách tự động chèn vào đầu trang
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
    // Cấu hình kết nối tới kho dữ liệu Firebase của bạn
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

    // Lắng nghe dữ liệu thay đổi trên mạng để cập nhật về màn hình
    database.ref('dulieu_nhatky/').on('value', (snapshot) => {
        const data = snapshot.val();
        if (data) {
           console.log("Đã nhận dữ liệu đồng bộ mới nhất từ đám mây!");
           // Tự động tìm và điền vào các ô nhập liệu nếu có
           const inputs = document.querySelectorAll('input, textarea, select');
           inputs.forEach(input => {
               if(data[input.id || input.name]) {
                   input.value = data[input.id || input.name];
               }
           });
        }
    });

    // Lắng nghe sự kiện người dùng nhập liệu để tự động lưu lên mạng
    document.addEventListener('change', function(e) {
        if(e.target.matches('input, textarea, select')) {
            let key = e.target.id || e.target.name;
            if(key) {
                database.ref('dulieu_nhatky/' + key).set(e.target.value);
            }
        }
    });
}

// Chạy kích hoạt khi trang web tải xong
window.addEventListener('DOMContentLoaded', loadFirebase);
