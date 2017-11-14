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

		cd ${HOME}/AndroidStudioProjects/MyApplication && {
			./gradlew  assembleDebug && ./gradlew installDebug
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

	*)
		echo $0 emulator/log/compile/shell/studio
		
	;;
esac
