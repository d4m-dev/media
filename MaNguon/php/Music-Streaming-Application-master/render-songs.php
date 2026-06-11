<?php

$songs = $song_type_to_fetch;
?>
<?php if ($songs): ?>
    <div id="<?php echo $div_appender; ?>">
        <div id="<?php echo $div_appender; ?>-headers">
            <ul id="fav-artist-songs-headers" class="row">
                <li class="song-header-cnt col-sm-1">#</li>
                <li class="song-header-title col-sm-3">TIÊU ĐỀ</li>
                <li class="song-header-artist col-sm-2">Nghệ sĩ</li>
                <li class="song-header-rating col-sm-1">ĐÁNH GIÁ TB</li>
                <li class="song-header-duration col-sm-1">THỜI LƯỢNG</li>
                <li class="song-header-rate col-sm-1">ĐÁNH GIÁ</li>
                <li class="song-header-playlist">THÊM VÀO DANH SÁCH PHÁT</li>
            </ul>
            <?php foreach ($songs as $i => $arr): ?>
                <ul id ="nav-<?php echo $div_appender; ?>-<?php echo $i; ?>" class="row pay-load songs-list">
                    <li class="song-header-cnt col-sm-1"><?php echo $i + 1; ?></li>
                    <form id="nav-<?php echo $div_appender; ?>-<?php echo $arr['TrackId']; ?>" method="POST" action="#nav-<?php echo $div_appender; ?>-<?php echo $i; ?>">
                        <input type="hidden" name="user_play_track" id="user_play_track" value="<?php echo $arr['TrackId']; ?>"/>
                        <input type="hidden" name="artist-title" id="artist-title" value="<?php echo $arr['ArtistTitle']; ?>">
                        <li class="song-header-title col-sm-3">
                            <a onclick="document.getElementById('nav-<?php echo $div_appender; ?>-<?php echo $arr['TrackId']; ?>').submit();">
                                <?php echo ucwords($arr['TrackName']); ?>
                            </a>
                        </li>
                        <li class="song-header-artist col-sm-2"><a href="./artistbio.php?aname=<?php echo $arr['ArtistTitle']; ?>"><?php echo $arr['ArtistTitle']; ?></a></li>
                    </form>
                    <li class="song-header-rating col-sm-1"><?php echo number_format($arr['avg_rating'], 2, '.', ''); ?></li>
                    <li class="song-header-duration col-sm-1"><?php echo number_format(($arr['TrackDuration'] / 60000), 2, ':', ''); ?></li>
                    <form class="col-sm-1" id="rating-<?php echo $arr['TrackId']; ?>" method="POST" action="#nav-<?php echo $i; ?>">
                        <input type="hidden" value="<?php echo $arr['TrackId']; ?>" id="track-id-rating" name="track-id-rating"/>
                        <li class="">
                            <select id="rating-value" name="rating-value" onchange="document.getElementById('rating-<?php echo $arr['TrackId'] ?>').submit();">
                                <option value="1" >1</option>
                                <option value="2" >2</option>
                                <option value="3" >3</option>
                                <option value="4" >4</option>
                                <option value="5" >5</option>
                            </select>
                        </li>
                    </form>
                    <li>
                        <?php if (!is_null($arr['PlaylistId'])): ?>
                            <div id="<?php echo $div_appender; ?>-added-to-playlist"><span class="glyphicon glyphicon-ok-sign" style="color:green"></span></div>
                        <?php else: ?>
                            <div data-toggle="modal" data-target="#<?php echo $div_appender; ?>-add-to-playlist-modal-<?php echo $arr['TrackId']; ?>"><span class="glyphicon glyphicon-plus" style="color:blue"></span></div>
                            <div class="modal fade" id="<?php echo $div_appender; ?>-add-to-playlist-modal-<?php echo $arr['TrackId']; ?>" role="dialog">
                                <div class="modal-dialog">
                                    <!-- Modal content-->
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                                            <h4 class="modal-title">Thêm bài hát vào danh sách phát</h4>
                                        </div>
                                        <div class="modal-body">
                                            <?php if (isset($my_playlists)): ?>
                                                <form method="post" action="add-to-playlist.php" name="<?php echo $div_appender; ?>-add-to-playlist-for-<?php echo $arr['TrackId']; ?>" id="<?php echo $div_appender; ?>-add-to-playlist-for-<?php echo $arr['TrackId']; ?>">
                                                    <p>Bài hát: <?php echo $arr['TrackName']; ?></p>
                                                    <?php if($my_playlists):?>
                                                    <select id="usr-playlists" name="usr-playlists">
                                                        <option value="-1">Chọn danh sách phát</option>
                                                        <?php foreach ($my_playlists as $i => $v): ?>
                                                            <option value="<?php echo $v['PlaylistId']; ?>"><?php echo $v['PlaylistName']; ?></option>
                                                        <?php endforeach; ?>
                                                    </select>
                                                    <input type="submit" value="Thêm vào danh sách phát"/>
                                                    <input type="hidden" name="track-id-to-add" id="track-id-to-add" value="<?php echo $arr['TrackId']; ?>"/>
                                                    <?php else:?>
                                                    <span>Bạn chưa có danh sách phát nào! Tạo tại trang cá nhân của bạn</span>
                                                    <?php endif;?>
                                                </form>
                                            <?php endif; ?>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-default" data-dismiss="modal">Đóng</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                    <?php endif; ?>
                </ul>

            <?php endforeach; ?>
        </div>
    </div>
<?php endif; ?>
