// static/activities/hamburger.js
document.addEventListener('DOMContentLoaded', () => {
    const hamburgerBtn = document.querySelector('.hamburger');
    const sideMenu = document.getElementById('sideMenu');
    const closeBtn = document.querySelector('.close-btn');

    if (!hamburgerBtn || !sideMenu) return;

    function openMenu() {
        sideMenu.setAttribute('aria-hidden', 'false');
        sideMenu.classList.add('open');

        // メニュー内の最初の操作要素へフォーカス
        closeBtn?.focus();
    }

    function closeMenu() {
        // 🔴 ① 現在フォーカスされている要素を確実に外す
        if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
        }

        // ② フォーカスを安全な場所へ戻す
        hamburgerBtn.focus();

        // ③ 見た目を閉じる
        sideMenu.classList.remove('open');

        // ④ aria-hidden を付与
        sideMenu.setAttribute('aria-hidden', 'true');
    }

    // ☰ ボタン
    hamburgerBtn.addEventListener('click', (e) => {
        e.stopPropagation();

        const isOpen = sideMenu.getAttribute('aria-hidden') === 'false';
        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // × ボタン
    closeBtn?.addEventListener('click', closeMenu);

    // Escキーで閉じる
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sideMenu.classList.contains('open')) {
            closeMenu();
        }
    });
});
