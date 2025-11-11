APPDIR = hestia.AppDir
APPIMAGE = hestia-x86_64.AppImage

package_prepare:
	test ! -d venv && python -m venv venv || true
	mkdir -p target

package_appimage: package_prepare
	mkdir -p "${APPDIR}/opt"
	mkdir -p "${APPDIR}/usr/lib"
	cp -r hestia "${APPDIR}/opt"
	cp -r venv "${APPDIR}/usr/lib"
	cp build/* "${APPDIR}"
	chmod +x "${APPDIR}/AppRun"
	ARCH=x86_64 appimagetool "${APPDIR}"
	mv "${APPIMAGE}" target

clean:
	rm -rf target ${APPDIR}
