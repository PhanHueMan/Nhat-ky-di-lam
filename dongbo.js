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
    let isTyping = false;

    // Hàm thực hiện đổ dữ liệu từ mạng đè lên màn hình
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

    // 1. ÉP TẢI DỮ LIỆU LIÊN TỤC: Cứ 1 giây là ép dữ liệu mạng hiển thị ra màn hình, chống lệnh xóa cũ
    setInterval(() => {
        if (!isTyping) {
            forceFillData();
        }
    }, 1000);

    // Theo dõi khi người dùng bắt đầu gõ chữ thì tạm dừng ép dữ liệu về để không bị khựng
    document.addEventListener('input', function() {
        isTyping = true;
    });

    // 2. TỰ ĐỘNG LƯU: Cứ sau mỗi 2 giây là tự động quét 10 ô nhập liệu quăng lên mạng
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

window.addEventListener('DOMContentLoaded', loadFirebase);
