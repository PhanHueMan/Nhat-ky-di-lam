// Tải trực tiếp thư viện Firebase bằng thẻ script chuẩn gắn thẳng vào trang
(function() {
    var s1 = document.createElement('script');
    s1.src = "https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js";
    var s2 = document.createElement('script');
    s2.src = "https://gstatic.com";
    
    document.head.appendChild(s1);
    s1.onload = function() {
        document.head.appendChild(s2);
        s2.onload = function() {
            initFirebaseSync();
        };
    };
})();

function initFirebaseSync() {
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
  
    if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }
    const database = firebase.database();
    let isTyping = false;

    // Hàm tự động đổ dữ liệu từ mạng đè lên màn hình
    function forceFillData() {
        database.ref('dulieu_nhatky/').once('value').then((snapshot) => {
            const data = snapshot.val();
            if (data && !isTyping) {
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
    }

    // Chạy lệnh tải dữ liệu ngay khi kết nối mạng xong xuôi
    forceFillData();

    // ÉP TẢI DỮ LIỆU LIÊN TỤC: Cứ 1 giây là ép dữ liệu mạng hiển thị, chống lệnh xóa tự động cũ
    setInterval(() => {
        if (!isTyping) { forceFillData(); }
    }, 1000);

    // Lắng nghe người dùng gõ chữ
    document.addEventListener('input', function() {
        isTyping = true;
    });

    // TỰ ĐỘNG LƯU: Cứ sau 2 giây gõ xong là tự bốc toàn bộ dữ liệu quăng lên mạng
    setInterval(() => {
        if (isTyping) {
            let dataToSave = {};
            const inputs = document.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                let key = input.id || input.name;
                if (key) {
                    dataToSave[key] = input.type === 'checkbox' ? input.checked : input.value;
                }
            });
            
            database.ref('dulieu_nhatky/').update(dataToSave, (error) => {
                if (!error) {
                    isTyping = false;
                    console.log("Đã tự động lưu dữ liệu lên đám mây!");
                }
            });
        }
    }, 2000);
}
