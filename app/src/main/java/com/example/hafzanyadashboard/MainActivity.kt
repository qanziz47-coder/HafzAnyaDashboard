package com.example.hafzanyadashboard

import android.content.pm.ActivityInfo
import android.os.Bundle
import android.view.HapticFeedbackConstants
import android.view.ViewGroup

import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge

import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll

import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView

import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView

import com.example.hafzanyadashboard.ui.theme.HafzAnyaDashboardTheme

import kotlinx.coroutines.delay
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

import java.net.HttpURLConnection
import java.net.URL


// ==========================================================
// WARNA TEMA
// ==========================================================

val CardBackground = Color(0xFF1A1F2E)
val SpotifyCardBackground = Color(0xFF3A3F4E)
val AccentBlue = Color(0xFF2196F3)
val AccentGreen = Color(0xFF4CAF50)
val AccentPurple = Color(0xFF9C27B0)
val AccentOrange = Color(0xFFFF9800)
val AccentRed = Color(0xFFF44336)
val AccentCyan = Color(0xFF00BCD4)
val TextSecondary = Color(0xFF8B949E)


// ==========================================================
// FONT FAMILY
// ==========================================================

val Orbitron = FontFamily(
    Font(R.font.orbitron_regular, FontWeight.Normal),
    Font(R.font.orbitron_medium, FontWeight.Medium),
    Font(R.font.orbitron_bold, FontWeight.Bold)
)


// ==========================================================
// PLAYLIST VIDEO
// ==========================================================
val videoPlaylist = listOf(
    R.raw.anyas,
    R.raw.spy,
    R.raw.cl,
    R.raw.spw,
    R.raw.sp2
)


// ==========================================================
// DATA CLASS UNTUK TOMBOL
// ==========================================================

data class ButtonConfig(
    val icon: String,
    val label: String,
    val endpoint: String,
    val color: String
)

fun getIconRes(iconName: String): Int {
    return when (iconName) {
        "spotify" -> R.drawable.spotify
        "chrome" -> R.drawable.chrome
        "file" -> R.drawable.file
        "wa" -> R.drawable.wa
        "shutdown" -> R.drawable.shutdown
        "restart" -> R.drawable.restart
        "lock" -> R.drawable.lock
        "sleep" -> R.drawable.sleep
        "cmd" -> R.drawable.cmd
        "calc" -> R.drawable.calc
        "taskmgr" -> R.drawable.taskmgr
        "settings" -> R.drawable.settings
        "youtube" -> R.drawable.youtube
        "gmail" -> R.drawable.gmail
        "google" -> R.drawable.google
        "discord" -> R.drawable.discord
        "playpause" -> R.drawable.playpause
        "next" -> R.drawable.next
        "prev" -> R.drawable.prev
        else -> R.drawable.settings
    }
}

fun getAccentColor(colorName: String): Color {
    return when (colorName) {
        "green" -> AccentGreen
        "blue" -> AccentBlue
        "purple" -> AccentPurple
        "orange" -> AccentOrange
        "red" -> AccentRed
        "cyan" -> AccentCyan
        else -> AccentBlue
    }
}


// ==========================================================
// FUNGSI KIRIM PERINTAH KE PC
// ==========================================================

fun kirimPerintah(url: String) {
    Thread {
        try {
            val connection = URL(url).openConnection() as HttpURLConnection
            connection.requestMethod = "GET"
            connection.connectTimeout = 3000
            connection.readTimeout = 3000
            val responseCode = connection.responseCode
            println("HafzLog: Response Code = $responseCode dari $url")
            connection.inputStream.close()
            connection.disconnect()
        } catch (e: Exception) {
            println("HafzLog: Error = ${e.message}")
        }
    }.start()
}


// ==========================================================
// FUNGSI PARSING PROFILES
// ==========================================================

fun parseProfiles(json: String): Map<String, List<ButtonConfig>> {
    val result = mutableMapOf<String, List<ButtonConfig>>()

    try {
        val profileRegex = "\"([a-z-]+)\"\\s*:\\s*\\[(.*?)\\]".toRegex(RegexOption.DOT_MATCHES_ALL)

        profileRegex.findAll(json).forEach { profileMatch ->
            val profileName = profileMatch.groupValues[1]
            val buttonsJson = profileMatch.groupValues[2]

            val buttons = mutableListOf<ButtonConfig>()

            val buttonRegex = "\\{([^}]+)\\}".toRegex()
            buttonRegex.findAll(buttonsJson).forEach { buttonMatch ->
                val buttonContent = buttonMatch.groupValues[1]

                val icon = "\"icon\"\\s*:\\s*\"([^\"]+)\"".toRegex()
                    .find(buttonContent)?.groupValues?.get(1) ?: ""
                val label = "\"label\"\\s*:\\s*\"([^\"]+)\"".toRegex()
                    .find(buttonContent)?.groupValues?.get(1) ?: ""
                val endpoint = "\"endpoint\"\\s*:\\s*\"([^\"]+)\"".toRegex()
                    .find(buttonContent)?.groupValues?.get(1) ?: ""
                val color = "\"color\"\\s*:\\s*\"([^\"]+)\"".toRegex()
                    .find(buttonContent)?.groupValues?.get(1) ?: "blue"

                if (icon.isNotEmpty() && label.isNotEmpty()) {
                    buttons.add(ButtonConfig(icon, label, endpoint, color))
                }
            }

            result[profileName] = buttons
        }
    } catch (e: Exception) {
        println("HafzLog: Error parsing profiles: ${e.message}")
    }

    return result
}


// ==========================================================
// BACKGROUND GRID PATTERN
// ==========================================================

@Composable
fun GridPattern(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val gridSize = 40.dp.toPx()
        val lineColor = Color(0x15FFFFFF)

        var x = 0f
        while (x < size.width) {
            drawLine(
                color = lineColor,
                start = Offset(x, 0f),
                end = Offset(x, size.height),
                strokeWidth = 1f
            )
            x += gridSize
        }

        var y = 0f
        while (y < size.height) {
            drawLine(
                color = lineColor,
                start = Offset(0f, y),
                end = Offset(size.width, y),
                strokeWidth = 1f
            )
            y += gridSize
        }
    }
}


// ==========================================================
// FUNGSI FALLBACK
// ==========================================================

@Composable
fun FallbackButtons() {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Row(horizontalArrangement = Arrangement.Center) {
            AnimatedStreamDeckButton(
                iconRes = R.drawable.spotify,
                label = "Spotify",
                accentColor = AccentGreen,
                onClick = { kirimPerintah("http://192.168.1.11:5000/spotify") }
            )
            Spacer(modifier = Modifier.width(14.dp))
            AnimatedStreamDeckButton(
                iconRes = R.drawable.chrome,
                label = "Chrome",
                accentColor = AccentBlue,
                onClick = { kirimPerintah("http://192.168.1.11:5000/chrome") }
            )
        }
        Spacer(modifier = Modifier.height(14.dp))
        Row(horizontalArrangement = Arrangement.Center) {
            AnimatedStreamDeckButton(
                iconRes = R.drawable.file,
                label = "Files",
                accentColor = AccentOrange,
                onClick = { kirimPerintah("http://192.168.1.11:5000/file") }
            )
            Spacer(modifier = Modifier.width(14.dp))
            AnimatedStreamDeckButton(
                iconRes = R.drawable.wa,
                label = "WhatsApp",
                accentColor = AccentPurple,
                onClick = { kirimPerintah("http://192.168.1.11:5000/whatsapp") }
            )
        }
    }
}


// ==========================================================
// FUNGSI WARNA & ICON PROFIL
// ==========================================================

fun getProfileColor(profile: String): Color {
    return when (profile) {
        "chrome" -> AccentBlue
        "spotify" -> AccentGreen
        "gaming" -> AccentPurple
        "vscode" -> AccentBlue
        "cmd" -> AccentOrange
        "calculator" -> AccentBlue
        "files" -> AccentOrange
        "vlc" -> AccentOrange
        "word" -> AccentBlue
        "excel" -> AccentGreen
        "android-studio" -> AccentGreen
        else -> AccentCyan
    }
}

fun getProfileIcon(profile: String): Int {
    return when (profile) {
        "chrome" -> R.drawable.chrome
        "spotify" -> R.drawable.spotify
        "gaming" -> R.drawable.discord
        "vscode" -> R.drawable.cmd
        "cmd" -> R.drawable.cmd
        "calculator" -> R.drawable.calc
        "files" -> R.drawable.file
        "vlc" -> R.drawable.playpause
        "word" -> R.drawable.word
        "excel" -> R.drawable.execl
        "android-studio" -> R.drawable.android
        else -> R.drawable.settings
    }
}


// ==========================================================
// MAIN ACTIVITY
// ==========================================================

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {

        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        WindowCompat.setDecorFitsSystemWindows(window, false)
        WindowInsetsControllerCompat(window, window.decorView).apply {
            hide(WindowInsetsCompat.Type.systemBars())
            systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        }

        setContent {
            HafzAnyaDashboardTheme {
                Dashboard()
            }
        }
    }
}


// ==========================================================
// DASHBOARD
// ==========================================================

@Composable
fun Dashboard() {

    // JAM DAN TANGGAL
    var currentTime by remember { mutableStateOf("") }
    var currentDate by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        while (true) {
            val now = Date()
            currentTime = SimpleDateFormat("HH:mm", Locale.getDefault()).format(now)
            currentDate = SimpleDateFormat("EEEE, dd MMM yyyy", Locale.getDefault()).format(now)
            delay(1000)
        }
    }

    val context = LocalContext.current

    // BATTERY
    var batteryLevel by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) {
        while (true) {
            val batteryManager =
                context.getSystemService(android.content.Context.BATTERY_SERVICE)
                        as android.os.BatteryManager
            batteryLevel = batteryManager.getIntProperty(
                android.os.BatteryManager.BATTERY_PROPERTY_CAPACITY
            )
            delay(5000)
        }
    }

    // STATE VIDEO
    var videoIndex by remember { mutableStateOf(0) }
    var mode by remember { mutableStateOf("video") }
    var videoFinished by remember { mutableStateOf(false) }

    // STATS PC (CPU & RAM)
    var cpuUsage by remember { mutableStateOf(0) }
    var ramUsage by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) {
        while (true) {
            try {
                val result = withContext(Dispatchers.IO) {
                    val url = URL("http://192.168.1.11:5000/stats")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 10000
                    connection.readTimeout = 10000
                    connection.connect()
                    val response = connection.inputStream.bufferedReader().use { it.readText() }
                    connection.disconnect()
                    response
                }

                val cpuRegex = "\"cpu\"\\s*:\\s*(\\d+)".toRegex()
                val ramRegex = "\"ram\"\\s*:\\s*(\\d+)".toRegex()

                val cpu = cpuRegex.find(result)?.groupValues?.get(1)?.toIntOrNull() ?: 0
                val ram = ramRegex.find(result)?.groupValues?.get(1)?.toIntOrNull() ?: 0

                cpuUsage = cpu
                ramUsage = ram
            } catch (e: Exception) {
                println("HafzLog: Error stats: ${e.javaClass.simpleName}")
            }
            delay(5000)
        }
    }

    // UPTIME PC
    var uptime by remember { mutableStateOf("0:0") }

    LaunchedEffect(Unit) {
        while (true) {
            try {
                val result = withContext(Dispatchers.IO) {
                    val url = URL("http://192.168.1.11:5000/uptime")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 10000
                    connection.readTimeout = 10000
                    connection.connect()
                    val response = connection.inputStream.bufferedReader().use { it.readText() }
                    connection.disconnect()
                    response
                }

                val uptimeRegex = "\"uptime\"\\s*:\\s*\"([^\"]+)\"".toRegex()
                uptime = uptimeRegex.find(result)?.groupValues?.get(1) ?: "0:0"
            } catch (e: Exception) {
                println("HafzLog: Error uptime: ${e.javaClass.simpleName}")
            }
            delay(60_000)
        }
    }

    // ACTIVE PROFILE
    var activeProfile by remember { mutableStateOf("default") }
    var activeApp by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        while (true) {
            try {
                val result = withContext(Dispatchers.IO) {
                    val url = URL("http://192.168.1.11:5000/active-app")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 10000
                    connection.readTimeout = 10000
                    connection.connect()
                    val response = connection.inputStream.bufferedReader().use { it.readText() }
                    connection.disconnect()
                    response
                }

                val appRegex = "\"app\"\\s*:\\s*\"([^\"]*)\"".toRegex()
                val profileRegex = "\"profile\"\\s*:\\s*\"([^\"]*)\"".toRegex()

                val app = appRegex.find(result)?.groupValues?.get(1) ?: ""
                val profile = profileRegex.find(result)?.groupValues?.get(1) ?: "default"

                if (app != activeApp || profile != activeProfile) {
                    activeApp = app
                    activeProfile = profile
                    println("HafzLog: Active app = '$app' -> profile = '$profile'")
                }
            } catch (e: Exception) {
                println("HafzLog: Error active-app: ${e.javaClass.simpleName}")
            }
            delay(3000)
        }
    }

    // PROFILE BUTTONS
    var profileButtons by remember {
        mutableStateOf(mapOf<String, List<ButtonConfig>>())
    }

    LaunchedEffect(Unit) {
        while (true) {
            try {
                val result = withContext(Dispatchers.IO) {
                    val url = URL("http://192.168.1.11:5000/profiles")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 10000
                    connection.readTimeout = 10000
                    connection.connect()
                    val response = connection.inputStream.bufferedReader().use { it.readText() }
                    connection.disconnect()
                    response
                }

                val parsed = parseProfiles(result)
                if (parsed.isNotEmpty()) {
                    profileButtons = parsed
                    println("HafzLog: Profiles loaded: ${parsed.keys}")
                }
            } catch (e: Exception) {
                println("HafzLog: Error profiles: ${e.javaClass.simpleName} - ${e.message}")
            }
            delay(30_000)
        }
    }

    // VIDEO PLAYER
    val exoPlayer = remember {
        ExoPlayer.Builder(context)
            .build()
            .apply {
                repeatMode = ExoPlayer.REPEAT_MODE_OFF
                volume = 0f
                playWhenReady = true
            }
    }

    DisposableEffect(Unit) {
        onDispose { exoPlayer.release() }
    }

    DisposableEffect(exoPlayer) {
        val listener = object : Player.Listener {
            override fun onPlaybackStateChanged(playbackState: Int) {
                if (playbackState == Player.STATE_ENDED) {
                    videoFinished = true
                }
            }
        }
        exoPlayer.addListener(listener)
        onDispose {
            exoPlayer.removeListener(listener)
        }
    }

    // LOOP: VIDEO → JAM → VIDEO → JAM
    LaunchedEffect(Unit) {
        while (true) {
            mode = "video"
            videoFinished = false

            val currentVideoRes = videoPlaylist[videoIndex]
            exoPlayer.setMediaItem(
                MediaItem.fromUri(
                    "android.resource://${context.packageName}/$currentVideoRes"
                )
            )
            exoPlayer.prepare()
            exoPlayer.play()

            var waitTime = 0
            while (!videoFinished && waitTime < 300_000) {
                delay(500)
                waitTime += 500
            }

            mode = "clock"
            exoPlayer.pause()
            delay(12_000)

            videoIndex = (videoIndex + 1) % videoPlaylist.size
        }
    }

    val scrollState = rememberScrollState()

    // ==================================================
    // TAMPILAN DASHBOARD (DENGAN GRID PATTERN)
    // ==================================================
    Box(modifier = Modifier.fillMaxSize()) {
        // 1. Background Gradient
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.linearGradient(
                        colors = listOf(
                            Color(0xFF0A0E1A),
                            Color(0xFF1A1F3A),
                            Color(0xFF0D1117)
                        ),
                        start = Offset(0f, 0f),
                        end = Offset(1000f, 2000f)
                    )
                )
        )

        // 2. Grid Pattern (dengan pointerInput agar tidak menyerap gesture scroll)
        GridPattern(
            modifier = Modifier
                .fillMaxSize()
                .pointerInput(Unit) {
                    awaitPointerEventScope {
                        while (true) {
                            awaitPointerEvent()
                        }
                    }
                }
        )

        // 3. Konten Utama
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState)
                .padding(16.dp)
        ) {

            // ==================================================
            // INDIKATOR PROFIL
            // ==================================================
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Start
            ) {
                val profileColor = getProfileColor(activeProfile)
                val profileIcon = getProfileIcon(activeProfile)

                Row(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .background(profileColor.copy(alpha = 0.15f))
                        .border(
                            width = 1.5.dp,
                            color = profileColor.copy(alpha = 0.6f),
                            shape = RoundedCornerShape(20.dp)
                        )
                        .padding(horizontal = 10.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Image(
                        painter = painterResource(id = profileIcon),
                        contentDescription = activeProfile,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = activeProfile.uppercase(),
                        color = profileColor,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.sp,
                        fontFamily = Orbitron
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // HALAMAN 1
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // AREA KIRI
                Column(
                    modifier = Modifier
                        .weight(1.6f)
                        .padding(horizontal = 4.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .aspectRatio(16f / 9f)
                            .clip(RoundedCornerShape(20.dp))
                            .background(Color.Black)
                            .border(
                                2.dp,
                                AccentBlue.copy(alpha = 0.5f),
                                RoundedCornerShape(20.dp)
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        if (mode == "video") {
                            AndroidView(
                                factory = { ctx ->
                                    PlayerView(ctx).apply {
                                        player = exoPlayer
                                        useController = false
                                        resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
                                        layoutParams = ViewGroup.LayoutParams(
                                            ViewGroup.LayoutParams.MATCH_PARENT,
                                            ViewGroup.LayoutParams.MATCH_PARENT
                                        )
                                        isClickable = false
                                        isFocusable = false
                                    }
                                },
                                modifier = Modifier
                                    .fillMaxSize()
                                    .pointerInput(Unit) {
                                        awaitPointerEventScope {
                                            while (true) {
                                                awaitPointerEvent()
                                            }
                                        }
                                    }
                            )
                        } else {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(
                                    text = currentTime,
                                    color = AccentBlue,
                                    fontSize = 90.sp,
                                    fontWeight = FontWeight.Bold,
                                    fontFamily = Orbitron
                                )
                                Text(
                                    text = currentDate,
                                    color = TextSecondary,
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Medium,
                                    fontFamily = Orbitron
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    // INFO PANEL
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0x22FFFFFF))
                                .border(1.dp, AccentGreen.copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Text(
                                text = "🔋 $batteryLevel%",
                                color = if (batteryLevel > 20) AccentGreen else Color.Red,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                fontFamily = Orbitron
                            )
                        }

                        Spacer(modifier = Modifier.width(8.dp))

                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0x22FFFFFF))
                                .border(
                                    1.dp,
                                    when {
                                        cpuUsage > 80 -> AccentRed
                                        cpuUsage > 50 -> AccentOrange
                                        else -> AccentBlue
                                    }.copy(alpha = 0.4f),
                                    RoundedCornerShape(12.dp)
                                )
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Text(
                                text = "CPU $cpuUsage%",
                                color = when {
                                    cpuUsage > 80 -> AccentRed
                                    cpuUsage > 50 -> AccentOrange
                                    else -> AccentGreen
                                },
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                fontFamily = Orbitron
                            )
                        }

                        Spacer(modifier = Modifier.width(8.dp))

                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0x22FFFFFF))
                                .border(
                                    1.dp,
                                    when {
                                        ramUsage > 80 -> AccentRed
                                        ramUsage > 50 -> AccentOrange
                                        else -> AccentBlue
                                    }.copy(alpha = 0.4f),
                                    RoundedCornerShape(12.dp)
                                )
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Text(
                                text = "RAM $ramUsage%",
                                color = when {
                                    ramUsage > 80 -> AccentRed
                                    ramUsage > 50 -> AccentOrange
                                    else -> AccentGreen
                                },
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                fontFamily = Orbitron
                            )
                        }

                        Spacer(modifier = Modifier.width(8.dp))

                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0x22FFFFFF))
                                .border(1.dp, AccentPurple.copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Text(
                                text = "⏱️ ${uptime.replace(":", "h ")}m",
                                color = AccentPurple,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                fontFamily = Orbitron
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.width(20.dp))

                // AREA KANAN (TOMBOL DINAMIS)
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 4.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    AnimatedContent(
                        targetState = activeProfile,
                        transitionSpec = {
                            (fadeIn(animationSpec = tween(300)) +
                                    slideInHorizontally(
                                        animationSpec = tween(300),
                                        initialOffsetX = { it / 2 }
                                    )) togetherWith
                                    (fadeOut(animationSpec = tween(300)) +
                                            slideOutHorizontally(
                                                animationSpec = tween(300),
                                                targetOffsetX = { -it / 2 }
                                            ))
                        },
                        label = "profile_transition"
                    ) { profile ->
                        val currentButtons = profileButtons[profile]
                            ?: profileButtons["default"]
                            ?: emptyList()

                        if (currentButtons.isEmpty()) {
                            FallbackButtons()
                        } else {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                currentButtons.chunked(2).forEach { rowButtons ->
                                    Row(horizontalArrangement = Arrangement.Center) {
                                        rowButtons.forEach { button ->
                                            AnimatedStreamDeckButton(
                                                iconRes = getIconRes(button.icon),
                                                label = button.label,
                                                accentColor = getAccentColor(button.color),
                                                backgroundColor = if (profile == "spotify") {
                                                    SpotifyCardBackground
                                                } else {
                                                    CardBackground
                                                },
                                                onClick = {
                                                    kirimPerintah("http://192.168.1.11:5000${button.endpoint}")
                                                }
                                            )
                                            Spacer(modifier = Modifier.width(14.dp))
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(14.dp))
                                }
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // HALAMAN 2: SYSTEM CONTROL
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.shutdown,
                    label = "Shutdown",
                    accentColor = AccentRed,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/shutdown") }
                )
                Spacer(modifier = Modifier.width(14.dp))
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.restart,
                    label = "Restart",
                    accentColor = AccentOrange,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/restart") }
                )
                Spacer(modifier = Modifier.width(14.dp))
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.lock,
                    label = "Lock PC",
                    accentColor = AccentCyan,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/lock") }
                )
                Spacer(modifier = Modifier.width(14.dp))
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.sleep,
                    label = "Sleep",
                    accentColor = AccentPurple,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/sleep") }
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            // HALAMAN 3: PC TOOLS
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.cmd,
                    label = "CMD",
                    accentColor = AccentOrange,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/cmd") }
                )
                Spacer(modifier = Modifier.width(14.dp))
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.calc,
                    label = "Calculator",
                    accentColor = AccentBlue,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/calc") }
                )
                Spacer(modifier = Modifier.width(14.dp))
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.taskmgr,
                    label = "Task Manager",
                    accentColor = AccentRed,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/taskmgr") }
                )
                Spacer(modifier = Modifier.width(14.dp))
                AnimatedStreamDeckButton(
                    iconRes = R.drawable.settings,
                    label = "Settings",
                    accentColor = AccentBlue,
                    onClick = { kirimPerintah("http://192.168.1.11:5000/settings") }
                )
            }

            Spacer(modifier = Modifier.height(30.dp))
        }
    }
}


// ==========================================================
// COMPONENT TOMBOL ANIMASI
// ==========================================================

@Composable
fun AnimatedStreamDeckButton(
    iconRes: Int,
    label: String,
    accentColor: Color,
    backgroundColor: Color = CardBackground,
    onClick: () -> Unit
) {

    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()

    val scale by animateFloatAsState(
        targetValue = if (isPressed) 0.92f else 1f,
        animationSpec = tween(durationMillis = 100),
        label = "scale"
    )

    val glowAlpha by animateFloatAsState(
        targetValue = if (isPressed) 1f else 0.5f,
        animationSpec = tween(durationMillis = 150),
        label = "glow"
    )

    val view = LocalView.current

    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier
                .scale(scale)
                .width(120.dp)
                .height(120.dp)
                .shadow(
                    elevation = if (isPressed) 0.dp else 6.dp,
                    shape = RoundedCornerShape(20.dp),
                    ambientColor = accentColor.copy(alpha = 0.3f),
                    spotColor = accentColor.copy(alpha = 0.5f)
                )
                .clip(RoundedCornerShape(20.dp))
                .background(
                    Brush.linearGradient(
                        colors = listOf(
                            backgroundColor,
                            backgroundColor.copy(alpha = 0.85f)
                        )
                    )
                )
                .border(
                    width = 2.dp,
                    color = accentColor.copy(alpha = glowAlpha),
                    shape = RoundedCornerShape(20.dp)
                )
        ) {
            Button(
                onClick = {
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    onClick()
                },
                interactionSource = interactionSource,
                modifier = Modifier.fillMaxSize(),
                shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent
                ),
                contentPadding = androidx.compose.foundation.layout.PaddingValues(0.dp)
            ) {
                Image(
                    painter = painterResource(id = iconRes),
                    contentDescription = label,
                    modifier = Modifier.size(60.dp)
                )
            }
        }

        Spacer(modifier = Modifier.height(4.dp))

        Text(
            text = label,
            color = TextSecondary,
            fontSize = 11.sp,
            fontWeight = FontWeight.Medium,
            fontFamily = Orbitron
        )
    }
}