plugins {
    java
    id("org.jetbrains.intellij.platform") version "2.19.0"
}

group = providers.gradleProperty("pluginGroup").get()
version = providers.gradleProperty("pluginVersion").get()

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Set `platformLocalPath` (e.g. in ~/.gradle/gradle.properties) to build against an installed IDE
        // instead of downloading one.
        val localPath = providers.gradleProperty("platformLocalPath").orNull
        if (localPath.isNullOrBlank()) {
            intellijIdea(providers.gradleProperty("platformVersion"))
        } else {
            local(localPath)
        }
        pluginVerifier()
    }
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

intellijPlatform {
    buildSearchableOptions = false
    instrumentCode = false

    pluginConfiguration {
        version = providers.gradleProperty("pluginVersion")
        ideaVersion {
            sinceBuild = providers.gradleProperty("pluginSinceBuild")
            untilBuild = provider { null }
        }
    }

    pluginVerification {
        ides {
            recommended()
        }
    }
}
