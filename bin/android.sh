#!/usr/bin/env bash

case $1 in 
	emulator)
		cd ${HOME}/Android/Sdk/tools && {
			./emulator -data /home/tww/Android/Sdk/system-images/android-19/google_apis/x86/userdata.img -avd Nexus_5X_API_19
		}
	;;

	log)
		cd ${HOME}/Android/Sdk/platform-tools && {
			./adb -s emulator-5556 logcat
		}
	;;

	compile)
		shift

		version=${1:-Debug}

		cd ${HOME}/AndroidStudioProjects/MyApplication && {
			./gradlew  assemble$version && ./gradlew install$version
		}
	;;

	shell)
		cd ${HOME}/Android/Sdk/platform-tools && {
			./adb -s emulator-5556 shell
		}
	;;

	studio)
		cd ${HOME}/usr/share/android-studio/bin && {
			./studio.sh
		}
	;;

	clean)
		shift
		cd ${HOME}/AndroidStudioProjects/MyApplication && {
			./gradlew clean $*
		}
	;;

	*)
		echo $0 emulator/log/compile/shell/studio/clean
		
	;;
esac
